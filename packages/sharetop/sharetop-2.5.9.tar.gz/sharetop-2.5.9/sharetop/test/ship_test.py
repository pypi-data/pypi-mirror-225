from sharetop.core.ship.ship_detail import get_ship_indicators

token = "73b6539c457a646e"

d = get_ship_indicators(token, org_name="中国", ship_indicators="1", is_explain=True)

print(d)
