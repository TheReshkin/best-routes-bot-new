code_cities = {'москва': "MOW", 'санкт-петербург': "LED", 'новосибирск': "OLB"}


def city_to_iata(city: str):
    code = code_cities.get(city.lower())
    if code is not None:
        return code
    else:
        return None
