import requests
import bs4
import aiohttp
#import asyncio

class Kroky:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.main_url = "https://www.kroky.si/2016/"
        self.menu = []
        self.session = requests.Session()
        self.response = self.session.post(self.main_url, data={"username": self.username, "password": self.password},
                                          params={"mod": "register", "action": "login"})
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.response_status = not soup.find('font', color="Red")

    def get_menu(self, pos, day=("pon", "tor", "sre", "cet", "pet", "sob")):
        menu = {}

        if self.response_status:

            # Access the main URL using the same session
            main_response = self.session.get(self.main_url, params={"mod": "register", "action": "order", "pos": pos-1})

            if main_response.ok:
                soup = bs4.BeautifulSoup(main_response.text, "html.parser")
                for i in day:
                    day_menu = []
                    for k in range(1, 12):
                        for j in soup.find_all("td", class_=f"st_menija_{k}_{i}"):
                            try:
                                xxl_element = j.find(class_="xxl")
                                if xxl_element:
                                    input_element = xxl_element.find("input")
                                    xxl_checked = True if input_element and input_element.get(
                                        "checked") == "checked" else False
                                else:
                                    xxl_checked = False

                                day_menu.append({
                                    f"meni": j.find("span", class_="lepo_ime").text,
                                    "selected": True if j.find("input").has_attr("checked") else False,
                                    "xxl": xxl_checked
                                })
                            except:
                                pass
                    menu[i] = day_menu

                self.menu = menu
                return menu
            else:
                return f"Failed to access main URL: {main_response.status_code}"
        else:
            return f"Login failed: napacni vhodni podatki"

    def select_meal(self, date, id):

        selection_data = {
            "c": int(id),
            "date": str(date),
        }

        selection_response = self.session.post(self.main_url,
            data=selection_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            params={"mod": "register", "action": "user2date2menu"})

        if not selection_response.ok:
            return f"Failed to select meal with status code: {selection_response.status_code}", 500

        return "Meal selected successfully!"

    def user_info(self):
        if self.response_status:
            soup = bs4.BeautifulSoup(self.session.get(self.main_url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                    params= {"mod": "register", "action": "editProfile"}).text, "html.parser")

        return {
                "name": soup.find_all('td')[1].string.strip() if soup.find_all('td')[1].string.strip() else None,
                "surename": soup.find_all('td')[3].string.strip() if soup.find_all('td')[3].string.strip() else None,
                "username": soup.find('b').string if soup.find('b').string else None,
                "email": soup.find('input', id='f_email')['value'],
                "main_menu": soup.find('select', {'name': 'privzeti'}).find('option', selected=True)['value'] if soup.find('select', {'name': 'privzeti'}).find('option', selected=True)['value'] else None
            }


    def change_password(self, password: str, password2: str):
        if self.response_status:
            main_response = self.session.get(self.main_url, params={"mod": "register", "action": "editProfile"})
            if main_response.ok:
                selection_response = self.session.post(self.main_url,
                    data={"password": password,"password2": password2,},
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                    params={"mod": "register", "action": "editProfile"})

                if selection_response.ok:
                    return "dela"
                return "ne dela!"


class KrokyAsync:
    def __init__(self, username, password):
        self.main_url = "https://www.kroky.si/2016/"
        self.menu = []
        self.username = username
        self.password = password
        self.session = None
        self.response_status = False

    @classmethod
    async def create(cls, username, password):
        self = cls(username, password)
        await self.initialize()
        return self

    async def initialize(self):
        self.session = aiohttp.ClientSession()
        self.response_status = await self.login(self.username, self.password)

    async def login(self, username, password):
        async with self.session.post(self.main_url, data={"username": self.username, "password": self.password},
                                     params={"mod": "register", "action": "login"}) as response:
            soup = bs4.BeautifulSoup(await response.text(), "html.parser")
            return not soup.find('font', color="Red")

    async def get_menu(self, pos, day=("pon", "tor", "sre", "cet", "pet", "sob")):
        menu = {}

        if self.response_status:
            async with self.session.get(self.main_url, params={"mod": "register", "action": "order", "pos": pos}) as main_response:
                if main_response.ok:
                    soup = bs4.BeautifulSoup(await main_response.text(), "html.parser")
                    for i in day:
                        day_menu = []
                        for k in range(1, 12):
                            for j in soup.find_all("td", class_=f"st_menija_{k}_{i}"):
                                try:
                                    xxl_element = j.find(class_="xxl")
                                    xxl_checked = bool(xxl_element and xxl_element.find("input", checked=True))

                                    day_menu.append({
                                        "meni": j.find("span", class_="lepo_ime").text,
                                        "selected": j.find("input").has_attr("checked"),
                                        "xxl": xxl_checked
                                    })
                                except:
                                    pass
                        menu[i] = day_menu
                    self.menu = menu
                    return menu
                else:
                    return f"Failed to access main URL: {main_response.status}"
        else:
            return "Login failed: napacni vhodni podatki"

    async def select_meal(self, date, id):
        selection_data = {
            "c": int(id),
            "date": str(date),
        }

        async with self.session.post(self.main_url,
                                     data=selection_data,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     params={"mod": "register", "action": "user2date2menu"}) as selection_response:

            if not selection_response.ok:
                return f"Failed to select meal with status code: {selection_response.status}", 500

        return "Meal selected successfully!"

    async def user_info(self):
        if not self.response_status:
            return "Login failed"

        async with self.session.get(self.main_url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                    params={"mod": "register", "action": "editProfile"}) as response:
            soup = bs4.BeautifulSoup(await response.text(), "html.parser")
            return {
                "name": soup.find_all('td')[1].string.strip() if soup.find_all('td')[1].string.strip() else None,
                "surename": soup.find_all('td')[3].string.strip() if soup.find_all('td')[3].string.strip() else None,
                "username": soup.find('b').string if soup.find('b').string else None,
                "email": soup.find('input', id='f_email')['value'],
                "main_menu": soup.find('select', {'name': 'privzeti'}).find('option', selected=True)['value'] if soup.find('select', {'name': 'privzeti'}).find('option', selected=True)['value'] else None
            }

    async def change_password(self, password: str, password2: str):
        if not self.response_status:
            return "Login failed"

        async with self.session.get(self.main_url, params={"mod": "register", "action": "editProfile"}) as main_response:
            if main_response.ok:
                async with self.session.post(self.main_url,
                                             data={"password": password, "password2": password2},
                                             headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                             params={"mod": "register", "action": "editProfile"}) as selection_response:
                    if selection_response.ok:
                        return "Password changed successfully"
                    return "Password change failed!"

    async def close_session(self):
        if self.session:
            await self.session.close()

    # Context manager to auto-close session
    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

