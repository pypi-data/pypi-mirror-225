from v7e_utils.agil_connect.agil_connect import AgilConnection


class PanelOwners(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/owners')

    def get_panel_owners(self, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, headers=headers)

    def get_panel_owners_as_list(self):
        try:
            owners = self.get_panel_owners()
            options = [(owner['id'], owner['name']) for owner in owners]
        except Exception as e:
            print(f"Error: {e}")
            options = []
        return options


class PanelBanks(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/banks')

    def get_panel_banks(self, realm, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, realm, headers=headers)

    def get_panel_banks_as_list(self, owner=None):
        try:
            banks = self.get_panel_banks(owner=owner)
            options = [(bank['id'], bank['description']) for bank in banks]
        except Exception as e:
            print(f"Error: {e}")
            options = []
        return options


class PanelDepartment(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/departments')

    def get_panel_department(self, realm, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, realm, headers=headers)


class PanelCountries(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/countries/')


    def get_panel_countries(self, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, headers=headers)


class PanelStates(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/states/')

    def get_panel_states(self, iso_country_code, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, iso_country_code, headers=headers)
    
    def get_states_by_id(self, state_id,headers=None):
        url = self.ensure_url(self.gateway_url, f'{self.api_endpoint}{state_id}/')
        return self.get_result(url, headers=headers)
    
class PanelDistricts(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/districts/')

    def get_panel_districts(self, county_id, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, county_id,headers=headers)

    def get_districts_by_id(self, district_id, headers=None):
        url = self.ensure_url(self.gateway_url, f'{self.api_endpoint}{district_id}/')
        return self.get_result(url, headers=headers)


class PanelCounties(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/counties/')

    def get_panel_counties(self, state_id, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, state_id, headers=headers)

    def get_counties_by_id(self, county_id, headers=None):
        url = self.ensure_url(self.gateway_url, f'{self.api_endpoint}{county_id}/')
        return self.get_result(url, headers=headers)


class PanelBusinessUnits(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/business-units/')

    def get_panel_business_units(self, realm, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, realm, headers=headers)
    
class PanelLegalRepresentative(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/legal-representative/')

    def get_panel_legal_representative(self, realm, headers=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url, realm,headers=headers)