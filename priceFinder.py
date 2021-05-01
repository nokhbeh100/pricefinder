from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

scCounter = 1
# time delay for showing
td = .25
#  time of each page loading
T = 1


def gotoElement(element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    
    

def highlight(priceElement, effect_time, color, border):
    """Highlights (blinks) a Selenium Webdriver element"""
    try:
        
        driver = priceElement._parent
        def apply_style(sty):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                  priceElement, sty)
        
        original_style = priceElement.get_attribute('style')
        gotoElement(priceElement)        
        apply_style("border: {0}px solid {1};".format(border, color))
        time.sleep(effect_time)
        apply_style(original_style)
    except:
        pass

def highlightAndScreenshot(priceElement, effect_time, color, border, name):
    """Highlights (blinks) a Selenium Webdriver element"""
    try:
        driver = priceElement._parent
        def apply_style(sty):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                  priceElement, sty)
        
        original_style = priceElement.get_attribute('style')
        gotoElement(priceElement)        
        apply_style("border: {0}px solid {1};".format(border, color))
        driver.save_screenshot(name)
        time.sleep(effect_time)
        apply_style(original_style)
    except:
        pass
    
def takeScreenshot(priceElement, val):
    global scCounter
    print(f"taking a screenshot {scCounter}")
    #driver.fullscreen_window() 
    
    highlightAndScreenshot(priceElement, td, 'red', '2', f"screenshot_{val}_{scCounter}.png")
    scCounter += 1        

def processPriceTagElement(priceElement):
    text = priceElement.text.strip()
    print(text)
    price_tag = ''.join( filter( lambda x: '0'<=x<='9' or x=='.', text))
    
    if price_tag:
        if len(list(filter(lambda x:x=='.',price_tag)))<=1: # should not contain multipe decimal points
                
            val = float(price_tag)
            print(f'val:{val}')
            takeScreenshot(priceElement, val)    
            return True
    return False

def processLink(link):

    #notvisited = False
    print(link)
    driver.get(link)
    time.sleep(T)
    mainElements = driver.find_elements_by_xpath(f"//*[contains(text(), '{sp[0]}')]")
    # the main element includes the name of the target procutct
    for mainElement in mainElements:
        if all([w in mainElement.text for w in sp]):
            print(f"mainElement:{mainElement.text}")
            saw = False
            # found a part that contains all parts that we searched for
            while not(saw):
                print("processing the high level")
                highlight(mainElement, td, 'blue', '2')
                priceElements = mainElement.find_elements_by_xpath(".//*[contains(text(), '$')]")
                print(len(priceElements))
                for priceElement in priceElements:
                    highlight(priceElement, td, 'green', '2')
                    if '$' in priceElement.text:
                        # saw a price
                        print("found a price tag")
                        saw = processPriceTagElement(priceElement)
                        if saw:
                            break # we only break if we took a screenshot
                if not(saw):
                    print('trying to go up')
                    try:                        
                        mainElement = mainElement.find_element_by_xpath('..')
                    except:
                        print("there is no up")
                        break # while
        

os.system('del *.png')

keywords = ['Buy', 'Price', 'price', 'buy']
#driver = webdriver.Chrome('chromedriver.exe')
driver = webdriver.Chrome()

#inp = input("give us a product:") 
inp = 'NVIDIA RTX 2080, AMD EPYC 7002'
for s in inp.split(','):
    
    print(f"searching for {s}")
    sp = s.split()
    
    #test for our code without the search part (also a good showcase)
    #processLink('https://www.amazon.ca/NVIDIA-GEFORCE-RTX-2080-Founders/dp/B07HWMDDMK')
    
    for keyword in keywords:
        s = keyword + ' ' + s.strip()
          
        s = s.replace(' ', '+')  
              
        driver.get("https://www.google.com/search?q=" + s + "&start=1") 
        
        
        
        links = []
        for link in driver.find_elements_by_tag_name('a'):
            links.append( link.get_attribute("href") )
        
        #notvisited = True
        for link in links:
            if link:
                if 'google' in link:# and notvisited:
                    continue
                processLink(link)         
            
    
    

driver.close()
#'$'

#for each page:
    #save price
    #take screenshot
