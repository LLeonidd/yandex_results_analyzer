from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
from urllib.parse import quote
from random import randint


def get_element_value(item, selector):
    """
    Get the text value of an element by a selector
    :param item: selenium object
    :param selector: selector
    :return: text value of an element by a selector
    """
    try:
        #return item.find_element_by_css_selector('.organic__url-text').text
        return item.find_element_by_css_selector(selector).text
    except StaleElementReferenceException:
        return
    except NoSuchElementException:
        return


def get_attribute_value(item, selector, attr):
    """
    Get the text value of an element attribute by a selector
    :param item: selenium object
    :param selector: selector
    :return: text value of an element attribute by a selector
    """
    try:
        return item.find_element_by_css_selector(selector).get_attribute(attr)
    except StaleElementReferenceException:
        return
    except NoSuchElementException:
        return


def get_search_results(key_request, ads=False):
    """
    Get query results in Yandex search engine by keyword
    :param key_request: keyword
    :param ads: Include advertising in the output dataset
    :return: object {
                'ads':[{'title':, 'root_url':, 'link':, 'position':,}, ...], # for advertising
                'results':[{'title':, 'root_url':, 'link':, 'position':,}, ...],
                'summary':{'ads_count':, 'result_count':, 'total_result_count':,}
                }
    """
    key_request = quote(key_request)
    driver.get(f"https://yandex.ru/search/?text={key_request}")
    time.sleep(randint(5,15))
    parents = driver.find_elements_by_css_selector('.serp-item')
    search_results = {
        'ads': [],
        'results': [],
        'summary': {}
    }
    parents = [item for item in parents if get_element_value(item, '.organic__url-text') != None ]
    for num, item in enumerate(parents):
        if item.find_elements_by_css_selector('.label_theme_direct').__len__() > 0:
            position_ad = num+1
            if ads:
                search_results['ads'].append(
                    {
                        'title': get_element_value(item, '.organic__url-text'),
                        'root_url': get_element_value(item, '.path__item b'),
                        'link': get_attribute_value(item, '.path__item', 'href'),
                        'position': position_ad,
                    }
                )
        else:
            position_result = num+1-position_ad
            search_results['results'].append(
                {
                    'title': get_element_value(item, '.organic__url-text'),
                    'root_url': get_element_value(item, '.path__item b'),
                    'link': get_attribute_value(item, '.path__item', 'href'),
                    'position': position_result,
                }
            )

        search_results['summary']['ads_count'] = search_results['ads'].__len__()
        search_results['summary']['results_count'] = search_results['results'].__len__()
        search_results['summary']['total_results_count'] = search_results['results'].__len__() + search_results['ads'].__len__()

    return search_results


if __name__ == '__main__':
    root_url = 'https://yandex.ru'
    profile = webdriver.FirefoxProfile()
    profile.set_preference("geo.prompt.testing", True)
    profile.set_preference("geo.prompt.testing.allow", True)
    profile.set_preference('geo.wifi.uri',
                           'data:application/json,{"location": {"lat": 45.0200, "lng": 38.5900}, "accuracy": 27000.0}')
    driver = webdriver.Firefox(firefox_profile=profile)

    print(
        get_search_results(key_request='Selenium forever', ads=True)
       )
    driver.close()