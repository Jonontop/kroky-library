import requests
import bs4


class Kroky:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.main_url = "https://www.kroky.si/2016/"
        self.menu = []
        self.session = requests.Session()
        self.response = self.session.post(self.main_url, data={"username": self.username, "password": self.password}, params={"mod": "register", "action": "login"})

    def get_menu(self, pos):
        day = ["pon", "tor", "sre", "cet", "pet", "sob"]
        menu = []


        if self.response.ok:
            print("Login successful")

            # Access the main URL using the same session
            main_response = self.session.get(self.main_url, params={"mod": "register", "action": "order", "pos": pos})

            if main_response.ok:
                soup = bs4.BeautifulSoup(main_response.text, "html.parser")
                for i in day:
                    day_menu = {}
                    day_menu[i] = []
                    for k in range(1, 12):
                        for j in soup.find_all("td", class_=f"st_menija_{k}_{i}"):
                            day_menu[i].append({
                                f"meni": j.find("span", class_="lepo_ime").text,
                                "selected": True if j.find("input").has_attr("checked") else False
                            })
                    menu.append(day_menu)

                self.menu = menu
                return menu
            else:
                return f"Failed to access main URL: {main_response.status_code}"
        else:
            return f"Login failed: {self.response.status_code}"

    def select_meal(self, date, id):

        selection_data = {
            "c": int(id),
            "date": str(date),
        }

        selection_response = self.session.post(self.main_url, data=selection_data,
                                          headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                          params={"mod": "register", "action": "user2date2menu"})

        if not selection_response.ok:
            return f"Failed to select meal with status code: {selection_response.status_code}", 500

        return "Meal selected successfully!"

