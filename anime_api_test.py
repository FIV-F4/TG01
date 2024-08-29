import requests


def get_anime(text):
    url = f'https://kitsu.io/api/edge/anime?filter[text]={text}'
    response = requests.get(url)
    if response.status_code == 200:
        anime_data = response.json()
        if anime_data['data']:
            return anime_data['data'][0]  # Возвращаем информацию о первом найденном аниме
        else:
            return None
    else:
        return None


if __name__ == '__main__':
    anime_name = 'Naruto'  # Замените на желаемое название аниме
    anime_info = get_anime(anime_name)
    if anime_info:
        title = anime_info['attributes']['canonicalTitle']
        synopsis = anime_info['attributes']['synopsis']
        show_type = anime_info['attributes']['showType']
        start_date = anime_info['attributes']['startDate']
        poster_image_url = anime_info['attributes']['posterImage']['medium']

        info = (
            f"Title: {title}\n"
            f"Type: {show_type}\n"
            f"Start Date: {start_date}\n"
            f"Synopsis: {synopsis}\n"
            f"Poster Image: {poster_image_url}\n"
        )

        print(info)
    else:
        print("Anime not found.")
