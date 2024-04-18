from speak_n_listen import speak, listen
import random
from requests_html import HTMLSession
from os import system
import re


def get_site(session):
    return session.get("https://www.coolmod.com/")


def hear_price():
    while True:
        try:
            guess = listen()
            price = float(guess.replace(" €", "").replace(" euros", "").replace(" con ", ".").replace(",", "."))
            return price
        except Exception:
            speak("No te he entendido")


def get_categories(main_site):
    all_categories = main_site.html.find(".subfamilylist")
    category_list = {}
    while len(category_list) < 5:
        category = random.choice(all_categories)
        while category.text == "Configura tu PC a Medida":
            category = random.choice(all_categories)
        sub_category_link = random.choice(list(category.links))
        sub_category_name = re.findall("https://www.coolmod.com/([A-Za-z0-9-]+)", sub_category_link)
        category_list.update({"{}".format(sub_category_name[0].replace("-", " ")): "{}".format(random.choice(list(category.links)))})
    return category_list


def category_selection(categories, opc):
    a = 0
    for category in categories:
        if a == opc:
            return categories[category]
        a += 1


def random_product_n_text(session, sub_category, main_site):

    sub_category_page = session.get(sub_category)

    # Get random product
    products = sub_category_page.html.find(".productInfo")
    if len(products) < 1:
        random_product_n_text(main_site, session, main_site)
    product = random.choice(products)
    product_text = list(product.text.split("\n"))
    if len(product_text) > 3:
        return product_text
    else:
        random_product_n_text(main_site, session, main_site)


def get_product_name(product_text):
    if len(product_text) > 11:
        return product_text[3]
    else:
        return product_text[1]


def get_product_price(product_text):
    if len(product_text) > 11:
        return float(product_text[11].replace(".", "").replace(" €", "").replace(",", "."))
    else:
        return float(product_text[3].replace(".", "").replace(" €", "").replace(",", "."))


def price_guesses():
    speak("Turno del jugador 1:")
    player_1_guess = hear_price()
    speak("Turno del jugador 2:")
    player_2_guess = hear_price()
    return player_1_guess, player_2_guess


def get_winner(product_price, player_1_approach, player_2_approach,
               player_1_guess, player_2_guess, player_1_points, player_2_points):
    if player_1_approach < player_2_approach:
        speak("El precio del producto es: {}. ¡Gana el jugador 1! ({})".format(product_price, player_1_guess))
        player_1_points += 1
    elif player_1_approach == player_2_approach:
        speak("El precio del producto es: {}. ¡Empate! ({})".format(product_price, player_1_guess))
    else:
        speak("El precio del producto es: {}. ¡Gana el jugador 2! ({})".format(product_price, player_2_guess))
        player_2_points += 1
        return player_1_points, player_2_points


def main():
    speak("¡Bienvenido al precio justo!\n"
          "Dos jugadores se enfrentan para ver quién se aproxima más al precio de un producto aleatorio en Coolmod")

    # Create session
    session = HTMLSession()
    main_site = get_site(session)

    # Game base
    n = 0
    player_1_points, player_2_points = 0, 0

    # Game starts. It is 5 rounds long
    while n != 4:
        system("cls")
        print("Jugador 1: {} puntos\n"
              "Jugador 2: {} puntos\n".format(player_1_points, player_2_points))

        # Select random category
        categories = get_categories(main_site)

        # Let user select category
        i = 1
        for item in categories.keys():
            print("{}: {}".format(i, item))
            i += 1

        sub_category = None
        while not sub_category:
            speak("Elige una categoría [1-5]: ")
            opc = int(input()) - 1
            try:
                if opc in range(5):
                    sub_category = category_selection(categories, opc)
            except Exception:
                pass

        # Select random product and get stats
        product_text = random_product_n_text(session, sub_category, main_site)

        # Get product characteristics
        product_name = get_product_name(product_text)
        product_price = get_product_price(product_text)

        # Product name and guess price
        speak(product_name)

        player_1_guess, player_2_guess = price_guesses()

        player_1_approach = abs(product_price - player_1_guess)
        player_2_approach = abs(product_price - player_2_guess)

        player_1_points, player_2_points = get_winner(product_price, player_1_approach, player_2_approach,
                                                      player_1_guess, player_2_guess, player_1_points, player_2_points)

        n += 1

    system("cls")
    if player_1_points > player_2_points:
        speak("¡Gana el jugador 1!\n\n"
              "Jugador 1: {} puntos\n"
              "Jugador 2: {} puntos".format(player_1_points, player_2_points))
    elif player_2_points > player_1_points:
        speak("¡Gana el jugador 2!\n\n"
              "Jugador 1: {} puntos\n"
              "Jugador 2: {} puntos".format(player_1_points, player_2_points))
    else:
        speak("¡Empate!\n\n"
              "Jugador 1: {} puntos\n"
              "Jugador 2: {} puntos".format(player_1_points, player_2_points))


if __name__ == "__main__":
    main()
