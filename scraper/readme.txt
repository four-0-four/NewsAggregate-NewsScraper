STEPS
############################################################################################
1)SCRAPE EACH ELEMENT
2)TEST MULTIPLE ARTICLES ESPECIALLY THE EDGE CASES
3)MAKE SURE THE CONTENT, DATE AND TITLE WAS SCRAPED CORRECTLY
4)SEE IF YOU CAN GET ALL THE CONFIG WITH WHAT WAS PLACED IN IT (SAVE TO JSON)
5)SAVE IT INSIDE THE DATABASE
  

TITLE SELECTOR
############################################################################################
SELECT THE TAG(E.G. H1) that contains the title directly with class

title_selector = ('h1',['vMjAx UdOCY WaKtx eHrJ mTgUP WimTs'])

NOTE: it has a list of classes, it is going to go through it one by one until it find the element. as soon as it does it return.
think of it like it if it has one of this element return

DATE SELECTOR
############################################################################################
SELECT THE TAG(E.G. div) that contains the date directly with class

date_selector = ('div',['VZTD mLASH'])

NOTE: it has a list of classes, it is going to go through it one by one until it find the element. as soon as it does it return.
think of it like it if it has one of this element return

IMAGE SELECTOR
############################################################################################
SELECT THE PARENT(E.G. div) OF THE IMAGE USING CLASS. THEN THE IMAGE WILL BE AUTOMATICALLY DETECTED

image_selector = ('div',['MediaPlaceholder'], 'src')

NOTE: it has a list of classes, it is going to go through it one by one until it find the element. as soon as it does it return.
think of it like it if it has one of this element return

CONTENT SELECTOR
############################################################################################
SELECT THE PARENT(E.G. div) THAT CONTAINS ALL THE CONTENT

content_selector = ('div',['xvlfx ZRifP TKoO eaKKC bOdfO'])

NOTE: it has a list of classes, it is going to go through it one by one until it find the element. as soon as it does it return.
think of it like it if it has one of this element return