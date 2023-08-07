import os
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from fake_useragent import UserAgent


DOWNLOAD_FOLDER = "boxes"
download_links = []


def get_random_user_agent():
    ua = UserAgent()
    return ua.random

headers = {'User-Agent': get_random_user_agent()}

def process_page(page):
    print(f'Processing page {page}')
    url = f'https://app.vagrantup.com/boxes/search?page={page}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        start_time = time.time()
        soup = BeautifulSoup(response.text, 'html.parser')
        boxes = soup.find_all('a', class_='list-group-item')
        div_elements = soup.find_all('div', class_='col-md-5')
        if boxes and div_elements:
            for box, div_element in zip(boxes, div_elements):
                small_element = div_element.find('small')
                box_version = small_element.text.strip()
                box_name = box['href'].split('/')[-3]
                version = box['href'].split('/')[-1]
                download_link = f"https://app.vagrantup.com{box['href']}/versions/{small_element.text.strip()}/providers/virtualbox.box"
                if download_link not in download_links:
                    download_links.append(download_link)
                    download_and_save_image(download_link, f"{box_name}.{version}.{box_version}.box")
        end_time = time.time() 
        elapsed_time = end_time - start_time
        print(f"Page {page} download time: {elapsed_time:.2f} seconds")
    else:
        print(f"Failed to fetch page {page} - Status code: {response.status_code}")

def download_and_save_image(download_link, filename):
    try:
        image_response = requests.get(download_link, headers=headers, stream=True)
        if image_response.status_code == 200:
            total_size = int(image_response.headers.get('content-length', 0))
            download_path = os.path.join(DOWNLOAD_FOLDER, filename)

            with open(download_path, 'wb') as file, tqdm(
                desc=filename, total=total_size, unit='iB', unit_scale=True, unit_divisor=1024
            ) as progress_bar:
                for data in image_response.iter_content(chunk_size=1024):
                    file.write(data)
                    progress_bar.update(len(data))
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {filename} - Status code: {image_response.status_code}")
    except Exception as e:
        print(f"Failed to download {filename} - {str(e)}")

def main():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    while True:
        try:
            pages_input = input("Enter the page number or range (e.g., 1 or 1-5): ")
            if '-' in pages_input:
                start_page, end_page = map(int, pages_input.split('-'))
                if start_page > end_page:
                    print("Invalid range: The start page should be less than or equal to the end page.")
                else:
                    break
            else:
                page_number = int(pages_input)
                if page_number > 0:
                    start_page, end_page = page_number, page_number
                    break
                else:
                    print("Invalid input: Page number should be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid page number or range.")

    for page in range(start_page, end_page + 1):
        process_page(page)

    with open(os.path.join(DOWNLOAD_FOLDER, 'download_links.txt'), 'w') as file:
        file.write('\n'.join(download_links))

    print('Done.')

if __name__ == "__main__":
    main()



