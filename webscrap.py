import requests
from bs4 import BeautifulSoup
import csv
req = requests.get('https://clutch.co/')

soup = BeautifulSoup(req.content,'html.parser')
domains = soup.find_all('a',class_ = "sitemap-nav__item")

def cutSpaces(st):
    s = ''
    for char in st:
        if char == ' ':
            break
        else :
            s += char
    return s.strip()
    
def findCompanyDetails(companyProfile):
    companyName = companyProfile.find('h1',class_="header-company--title")
    if companyName:
        companyName = companyName.a.text.strip()
    companyWebsite = companyProfile.find('li',class_="website-link-a")

    if companyWebsite:
        companyWebsite = companyWebsite.a['href']

    companyLocation = companyProfile.find('span',class_ = "city-name")
    if companyLocation:
        companyLocation = companyLocation.text

    companyContact = companyProfile.find('li',class_ = "quick-menu-details")
    if companyContact:
        companyContact = companyContact.a.text.strip()

    companyEmployees = companyProfile.find('div',attrs={"data-content" : "<i>Employees</i>"})
    if companyEmployees:
        companyEmployees = companyEmployees.span.text
    
    companyHourlyRate = companyProfile.find('div',attrs={"data-content" : "<i>Avg. hourly rate</i>"})
    if companyHourlyRate:
        companyHourlyRate = companyHourlyRate.span.text


    companyMinProjectSize = companyProfile.find('div',attrs={"data-content" : "<i>Min. project size</i>"})
    if companyMinProjectSize:
        companyMinProjectSize = companyMinProjectSize.find('span').text

    companyRating = companyProfile.find('span',class_ = "rating sg-rating__number")
    if companyRating:
        companyRating = companyRating.text.strip()

    reviews = companyProfile.find('a',class_ = "reviews-link sg-rating__reviews")
    if reviews:
        reviews = reviews.text.strip()
    companyReviews = cutSpaces(reviews) + " reviews"

    companyFoundedYear = companyProfile.find('div',attrs={"data-content" : "<i>Founded</i>"})
    if companyFoundedYear:
        companyFoundedYear = companyFoundedYear.span.text.split(' ')[1]
    # companyFocus = companyProfile.find('div',attrs={"data-content" : "<b>{}</b>"})
    companyVerification = companyProfile.find('div',class_="verification-status-wrapper")
    if companyVerification:
        companyVerification= companyVerification.text.strip()
    
    companyTagline = companyProfile.find('h2',class_="h2_title")
    if companyTagline:
        companyTagline = companyTagline.text.strip()
    
    companyStatus = companyProfile.find('div',class_="field field-name-status")
    if companyStatus:
        companyStatus = companyStatus.find('div',class_="field-item").text.strip()

    companyBankRuptcyStatus = companyProfile.find('div',class_="field field-name-bankruptcy")
    if companyBankRuptcyStatus:
        companyBankRuptcyStatus = companyBankRuptcyStatus.find('div',class_="field-item").text.strip()
    
    businessEntityName = companyProfile.find('div',class_="field field-name")
    if businessEntityName:
        businessEntityName = businessEntityName.find('div',class_="field-item").text.strip()
    
    companyDetail = {
        'Company' : companyName,
        'Business Entity Name': businessEntityName,
        'Domain' : companyDomain,
        'Website' : companyWebsite,
        'Location' : companyLocation,
        'Contact' : companyContact,
        'Rating' : companyRating,
        'Review Count' : companyReviews,
        'Hourly Rate' : companyHourlyRate,
        'Min Project Size' : companyMinProjectSize,
        'Employee Size' : companyEmployees,
        'Founded Year' : companyFoundedYear,
        'Status' : companyStatus,
        'Bank Ruptcy Status' :companyBankRuptcyStatus,
        'Tagline' : companyTagline,
        'Verification' : companyVerification,
    }
    return companyDetail




with open('result.csv','w',newline='',encoding="utf-8") as resultFile:
    fieldnames = ['Company','Business Entity Name' ,'Domain','Website','Location','Contact','Rating',
    'Review Count','Hourly Rate','Min Project Size','Employee Size',
    'Founded Year','Status','Bank Ruptcy Status','Tagline','Verification']
    csvWriter = csv.DictWriter(resultFile,fieldnames=fieldnames)
    csvWriter.writeheader()

    for domain in domains:
        domainLink = 'https://clutch.co'+ domain['href']

        domainReq = requests.get(domainLink)
        domainSoup = BeautifulSoup(domainReq.content,'html.parser')
        last_page = int(domainSoup.find('li',class_="page-item last").a['data-page'])

        for page in range(last_page+1):
            pageLink = domainLink + '?page=' + str(page)
            pageReq = requests.get(pageLink)
            pageSoup = BeautifulSoup(pageReq.content,'html.parser')

            companies = pageSoup.find('ul',class_='directory-list shortlist')
            companies = companies.find_all('li',class_ ="provider provider-row sponsor")

            companyDomain = domain.text.strip()
            
            for company in companies:
                companyProfileLink = "https://clutch.co" + company.find('li',class_="website-profile").a['href']
                profileRequest = requests.get(companyProfileLink)
                companyProfile = BeautifulSoup(profileRequest.content,'html.parser')

                companyDetail = findCompanyDetails(companyProfile)
                
                csvWriter.writerow(companyDetail)


