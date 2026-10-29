"""Lost Sanctum difficulty pools, from the AniimoTools client-data catalog."""
DIFFICULTIES=('Beginner','Hard','Nightmare','Chaos')
HIGH_TIER=(31,32,33,34,35,36,37,38,39,40,61,62)
POOLS={'Beginner':(53,54,55,56,57,58,59),
       'Hard':(41,42,45,48,49,50),'Nightmare':HIGH_TIER,'Chaos':HIGH_TIER}
ALL_LAYOUTS=tuple(sorted(set(n for pool in POOLS.values() for n in pool)))


def layouts_for(difficulty='Chaos'):
    return POOLS[difficulty]
