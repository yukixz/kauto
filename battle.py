import math
from enum import Enum


class BattleResult(Enum):
    Safe = 0
    Flagship_Damaged = 1
    Ship_Damaged = 2


class Ship:
    def __init__(self, now_hp=-1, max_hp=-1):
        self.now_hp = now_hp
        self.max_hp = max_hp

    def update_hp(self, damage):
        damage = math.floor(damage)
        if self.max_hp == -1:       # certain ship doesn't exist
            return damage
        if damage > 0:
            self.now_hp -= damage
            if self.now_hp < 0:
                self.now_hp = 0
                # TODO Repair item
        return damage

    def IsDamaged(self):
        if self.max_hp == -1 and self.now_hp == -1:
            return False
        if self.now_hp * 4 > self.max_hp:
            return False
        return True


def battle_analyze(battle_request, combined=0, verbose=False):
    '''
    Analyze the battle package and return current fleet status.
    ref: plugin-prophet@73ae09fc9a37754436cf7b5e642b0b1911c0999b
         https://github.com/poooi/plugin-prophet
    TODO: Repair item
    '''
    def kouku_attack(fleet, kouku):
        if 'api_fdam' in kouku:
            i = 0
            for damage in kouku['api_fdam']:
                if math.floor(damage) <= 0:
                    i += 1
                    continue
                fleet[i - 1].update_hp(damage)
                i += 1

    def support_attack(fleet, support):
        # Support attack won't affect sortie ships's hit points.
        # Ignored.
        pass

    def raigeki_attack(fleet, raigeki):
        i = 0
        for target in raigeki['api_erai']:
            if target <= 0:
                i += 1
                continue
            damage = raigeki['api_eydam'][i]
            fleet[target - 1].update_hp(damage)
            i += 1

    def hougeki_attack(fleet, hougeki):
        i = 0
        for damageFrom in hougeki['api_at_list']:
            if damageFrom <= 0:
                i += 1
                continue
            total_damage = 0
            for damage in hougeki['api_damage'][i]:
                total_damage += math.floor(damage)
            target = hougeki['api_df_list'][i][0]
            if target < 7:
                fleet[target - 1].update_hp(total_damage)
            i += 1

    # Get battle log
    if hasattr(battle_request, 'body'):
        battle_data = battle_request.body
    else:
        battle_data = battle_request

    # Initialize the fleet's hit points
    main_fleet = []
    escort_fleet = []
    for i in range(1, 7):
        if battle_data['api_maxhps'][i] < 0:
            ship = Ship()
        else:
            ship = Ship(now_hp=battle_data['api_nowhps'][i],
                        max_hp=battle_data['api_maxhps'][i])
        main_fleet.append(ship)
    if combined > 0 and battle_data.get('api_nowhps_combined', None) is not None:
        for i in range(1, 7):
            if battle_data['api_maxhps_combined'][i] < 0:
                ship = Ship()
            else:
                ship = Ship(now_hp=battle_data['api_nowhps_combined'][i],
                            max_hp=battle_data['api_maxhps_combined'][i])
            escort_fleet.append(ship)
    else:
        ship = Ship()
        for i in range(1, 7):
            escort_fleet.append(ship)

    # First kouku battle
    if battle_data.get('api_kouku', None) is not None:
        if battle_data['api_kouku'].get('api_stage3', None) is not None:
            kouku_attack(main_fleet, battle_data['api_kouku']['api_stage3'])
        if battle_data['api_kouku'].get('api_stage3_combined', None) is not None:
            kouku_attack(escort_fleet, battle_data['api_kouku']['api_stage3_combined'])

    # Second kouku battle
    if battle_data.get('api_kouku2', None) is not None:
        if battle_data['api_kouku2'].get('api_stage3', None) is not None:
            kouku_attack(main_fleet, battle_data['api_kouku2']['api_stage3'])
        if battle_data['api_kouku2'].get('api_stage3_combined', None) is not None:
            kouku_attack(escort_fleet, battle_data['api_kouku']['api_stage3_combined'])

    # Support battle is ignored for now

    # Opening battle
    if battle_data.get('api_opening_atack', None) is not None:
        if combined > 0:
            raigeki_attack(escort_fleet, battle_data['api_opening_atack'])
        else:
            raigeki_attack(main_fleet, battle_data['api_opening_atack'])

    # Night battle
    if battle_data.get('api_hougeki', None) is not None:
        if combined > 0:
            hougeki_attack(escort_fleet, battle_data['api_hougeki'])
        else:
            hougeki_attack(main_fleet, battle_data['api_hougeki'])

    # First hougeki battle
    if battle_data.get('api_hougeki1', None) is not None:
        if combined == 1 and combined == 3:
            hougeki_attack(escort_fleet, battle_data['api_hougeki1'])
        else:
            hougeki_attack(main_fleet, battle_data['api_hougeki1'])

    # Second hougeki battle
    if battle_data.get('api_hougeki2', None) is not None:
        hougeki_attack(main_fleet, battle_data['api_hougeki2'])

    # Combined hougeki battle
    if battle_data.get('api_hougeki3', None) is not None:
        if combined == 2:
            hougeki_attack(escort_fleet, battle_data['api_hougeki3'])
        else:
            hougeki_attack(main_fleet, battle_data['api_hougeki3'])

    # Raigeki battle
    if battle_data.get('api_raigeki', None) is not None:
        if combined > 0:
            raigeki_attack(escort_fleet, battle_data['api_raigeki'])
        else:
            raigeki_attack(main_fleet, battle_data['api_raigeki'])

    # Debug: print analyze result
    if verbose:
        print("Last_battle:")
        print("\tmain_feet:")
        for i in range(0,6):
            print('\t', main_fleet[i].now_hp, " / ", main_fleet[i].max_hp)
        if combined > 0:
            print("\tmain_feet:")
            for i in range(0,6):
                print('\t', escort_fleet[i].now_hp, " / ", escort_fleet[i].max_hp)

    # Calculate the result of the battle
    if main_fleet[0].IsDamaged():
        print("battle_analyze: Flagship_Damaged")
        return BattleResult.Flagship_Damaged
    # if escort_fleet[0].now_hp < escort_fleet[0].max_hp * 0.2500001:
    #     return BattleResult.Flagship_Damaged

    for i in range(1, 6):
        if main_fleet[i].IsDamaged() or escort_fleet[i].IsDamaged():
            print("battle_analyze: Ship_Damaged")
            return BattleResult.Ship_Damaged

    return BattleResult.Safe


def battle_timer(battle_request, combined=0):
    '''
    (TODO)Estimate durability of a battle.
    '''
    def kouku_time(kouku):
        eta = 0
        return eta

    def support_time(support):
        eta = 0
        return eta

    def raigeki_time(raigeki):
        eta = 0
        return eta

    def hougeki_time(hougeki):
        eta = 0
        return eta

    battle_data = battle_request.body
    total_time = 0

    # First kouku battle
    if battle_data.get('api_kouku', None) is not None:
        total_time += kouku_time(battle_data['api_kouku'])

    # Second kouku battle
    if battle_data.get('api_kouku2', None) is not None:
        total_time += kouku_time(battle_data['api_kouku2'])

    # Support battle
    if battle_data.get('api_support_info', None) is not None:
        total_time += support_time(battle_data['api_support_info'])

    # Opening battle
    if battle_data.get('api_opening_atack', None) is not None:
        total_time += raigeki_time(battle_data['api_opening_atack'])

    # Night battle
    if battle_data.get('api_hougeki', None) is not None:
        total_time += hougeki_time(battle_data['api_hougeki'])

    # First hougeki battle
    if battle_data.get('api_hougeki1', None) is not None:
        total_time += hougeki_time(battle_data['api_hougeki1'])

    # Second hougeki battle
    if battle_data.get('api_hougeki2', None) is not None:
        total_time += hougeki_time(battle_data['api_hougeki2'])

    # Combined hougeki battle
    if battle_data.get('api_hougeki3', None) is not None:
        total_time += hougeki_time(battle_data['api_hougeki3'])

    # Raigeki battle
    if battle_data.get('api_raigeki', None) is not None:
        total_time += raigeki_time(battle_data['api_raigeki'])

    return total_time


################################################################
#
#  Utils
#
################################################################


def port_has_damaged_ship(request):
    ''' Check whether there is damaged ship when returning to port.
    '''
    deck0 = request.body['api_deck_port'][0]['api_ship']
    ships = request.body['api_ship']
    for ship_id in deck0:
        if ship_id < 0:
            continue
        ship = None
        for shipd in ships:
            if shipd.get('api_id', -1) == ship_id:
                ship = shipd
                break
        if ship is None:
            raise Exception("Cannot find ship with id: %d" % ship_id)
        if any(['api_nowhp' not in ship,
                'api_maxhp' not in ship,
                4 * ship['api_nowhp'] <= ship['api_maxhp']
                ]):
            print("!! WARNING: Damaged ship found!")
            return True
    return False


def advance_has_damaged_ship(request):
    ''' Check whether there is damaged ship when advancing to next cell.
    '''
    ships = request.body['api_ship_data']
    for ship in ships:
        if any(['api_nowhp' not in ship,
                'api_maxhp' not in ship,
                4 * ship['api_nowhp'] <= ship['api_maxhp']
                ]):
            print("!! WARNING: Damaged ship found!")
            return True
    return False
