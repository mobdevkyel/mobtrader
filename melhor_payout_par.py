import time, math
from iqoptionapi.stable_api import IQ_Option


def is_asset_open(asset, all_opened_assets, mode='turbo'):
    return all_opened_assets[mode][asset]["open"]

def get_all_opened_assets(iqo_api):
    return iqo_api.get_all_open_time()

def get_all_profits(iqo_api):
    return iqo_api.get_all_profit()

def get_digital_profit(iqo_api, active, expiration):
    iqo_api.subscribe_strike_list(active, expiration)
    payout = iqo_api.get_digital_current_profit(active, expiration)
    while not payout:
        time.sleep(0.1)
        payout = iqo_api.get_digital_current_profit(active, expiration)
    iqo_api.unsubscribe_strike_list(active, expiration)
    return {'digital': math.floor(payout) / 100}

def most_profit_mode(iqo_api, pair, expiration, min_payout):
    _mpm = ['digital', .0, False]

    all_opened_assets = get_all_opened_assets(iqo_api)
    opened = dict()
    for mode in ['turbo', 'digital']:
        opened[mode] = is_asset_open(pair, all_opened_assets, mode)
    if opened['turbo'] or opened['digital']:
        profits = get_all_profits(iqo_api)
        if opened['digital']:
            if pair in profits:
                profits[pair].update(get_digital_profit(iqo_api, pair, expiration))
            else:
                profits[pair] = get_digital_profit(iqo_api, pair, expiration)
        priority_mode_list = []
        for k, v in opened.items():
            if v:
                priority_mode_list.append([k, profits[pair][k]])
        priority_mode_list = sorted(priority_mode_list, key=lambda x: x[1], reverse=True)
        if priority_mode_list:
            mode, best_payout = priority_mode_list[0]
            #print(mode, best_payout)
            print(mode)
            if best_payout >= min_payout:
                if mode == 'turbo':
                    _mpm[0], _mpm[1], _mpm[2] = 'turbo', best_payout, True
                else:
                    _mpm[0], _mpm[1], _mpm[2] = 'digital', best_payout, True
            else:
                #print(str(datetime.now()), "The payout for " + pair + " is below " + str(float(best_payout) * 100) + "%")
                _mpm[0], _mpm[1], _mpm[2] = 'payout', best_payout, False
        else:
            #print(str(datetime.now()), pair, "- Something went wrong. No items in your priority list :(")
            _mpm[0], _mpm[1], _mpm[2] = 'error', best_payout, False
    else:
        #print(str(datetime.now()), pair + " is closed now. :(")
        _mpm[0], _mpm[1], _mpm[2] = 'closed', best_payout, False

    return _mpm[0], _mpm[1], _mpm[2]


