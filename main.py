import requests
import bs4


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
        self.response_status = False if soup.find('font', color="Red") else True

    def get_menu(self, pos, day=("pon", "tor", "sre", "cet", "pet", "sob")):
        menu = []

        if self.response_status:
            print("Login successful")

            # Access the main URL using the same session
            main_response = self.session.get(self.main_url, params={"mod": "register", "action": "order", "pos": pos})

            if main_response.ok:
                soup = bs4.BeautifulSoup(main_response.text, "html.parser")
                for i in day:
                    day_menu = {i: []}
                    for k in range(1, 12):
                        for j in soup.find_all("td", class_=f"st_menija_{k}_{i}"):
                            day_menu[i].append({
                                f"meni": j.find("span", class_="lepo_ime").text,
                                "selected": True if j.find("input").has_attr("checked") else False
                            })
                    menu.append(day_menu)

                self.menu = menu
                return menu[0]
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


kroky = Kroky("pe-jon", "q460jk")
print(kroky.user_info())
