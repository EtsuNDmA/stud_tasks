# Данные из википедии
# https://en.wikipedia.org/wiki/United_States
# https://en.wikipedia.org/wiki/Great_Lakes

total_area_USA = 9833520  # km2

great_lakes_volumes = {
    'Erie': 480,
    'Huron': 3500,
    'Michigan': 4900,
    'Ontario': 1640,
    'Superior': 12000,
}  # km3

if __name__ == '__main__':
    total_volume = sum(great_lakes_volumes.values())
    height = total_volume / total_area_USA * 1000

    print('Площадь США (км2): {}'.format(total_area_USA))
    print('Объем великих озер (км3):')
    for lake, volume in great_lakes_volumes.items():
        print(' - {}: {}'.format(lake, volume))
    print('Суммарный объем (км3): {}'.format(total_volume))
    print('Высота слоя воды (м): {:.2f}'.format(height))
