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
            return (f"Login failed: napacni vhodni podatki")

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

    def user_info(self):
        if self.response_status:
            # Make sure you're sending the right data
            form_data = {
                "mod": "register",
                "action": "editProfile",
                # Add any other required fields here
            }

            url = self.session.get(self.main_url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                    params=form_data)

            # Check the response HTML
            soup = bs4.BeautifulSoup(url.text, "html.parser")

            # Extract the rows and data
            data = {}
            rows = soup.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 1:  # Ensure there are two cells in the row
                    label = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    data = {
                        "username": 
                    }
                    if label == "Ime:":
                        data["Ime"] = value
                    elif label == "Priimek:":
                        data["Priimek"] = value
                    elif label == "E-pošta:":
                        data["E-pošta"] = soup.find('input', id='f_email')['value']  
                    elif label == "Privzeti meni:":
                        menu = cells[1].find('select')
                        if menu:
                            selected_option = menu.find('option', selected=True)
                            if selected_option:
                                data["Privzeti meni"] = selected_option.text.strip()  # Meni 6 - is selected
                    elif label == "Uporabniško ime:":
                        data["Uporabniško ime"] = value

            # Print the extracted data
            for key, value in data.items():
                print(f"{key}: {value}")


    def change_password(self, password: str):
        if self.response.ok:
            main_response = self.session.get(self.main_url, params={"mod": "register", "action": "editProfile"})
            if main_response.ok:
                selection_data = {
                    "password": password,
                    "password2": password,
                }

        selection_response = self.session.post(self.main_url, data=selection_data,
                                               headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                               params={"mod": "register", "action": "editProfile"})

        if selection_response.ok:
            return "dela"
        return "ne dela!"


kroky = Kroky("pe-jon", "q460jk")
print(kroky.user_info())
