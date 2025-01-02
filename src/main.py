import json
from collections import defaultdict

def parse_log(log):
    players = defaultdict(lambda: {"kills": 0, "deaths": 0, "events": []})
    events = []
    
    for line in log.splitlines():
        parts = line.split()
        time = parts[0]
        event_type = parts[1].rstrip(':')
        details = ' '.join(parts[2:])
        
        if event_type == "Kill":
            killer_id = parts[2]
            victim_id = parts[3]
            killer = details.split(' killed ')[0].split()[-1]
            victim = details.split(' killed ')[1].split(' by ')[0]
            mod = details.split(' by ')[1]
            
            events.append({
                "time": time,
                "event_type": event_type,
                "killer_id": killer_id,
                "victim_id": victim_id,
                "killer": killer,
                "victim": victim,
                "mod": mod
            })
            
            if killer != "<world>":
                players[killer]["kills"] += 1
            players[victim]["deaths"] += 1
            players[killer]["events"].append({
                "time": time,
                "event_type": event_type,
                "victim": victim,
                "mod": mod
            })
            players[victim]["events"].append({
                "time": time,
                "event_type": event_type,
                "killer": killer,
                "mod": mod
            })
    
    return {"players": players, "events": events}

def main():
    log = """0:00 Kill: 1022 2 22: <world> killed Isgalamido by MOD_TRIGGER_HURT
0:15 Kill: 3 2 10: Isgalamido killed Dono da Bola by MOD_RAILGUN
1:00 Kill: 3 2 10: Isgalamido killed Zeh by MOD_RAILGUN"""
    
    parsed_log = parse_log(log)
    
    with open('quake_log.json', 'w') as f:
        json.dump(parsed_log, f, indent=4)
    
    print("Log parsed and saved to quake_log.json")

if __name__ == "__main__":
    main()