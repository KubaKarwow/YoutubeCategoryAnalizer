from pytrends.request import TrendReq

def getNewList(categoriesWatched):
    newCategoriesList = []
    for category in categoriesWatched:
        splitString = split_string(category)
        if type(splitString) is list:
            for item in splitString:
                newCategoriesList.append(item)
        else:
            newCategoriesList.append(split_string(category))
    return newCategoriesList

def split_string(input_string):
    # Check if the string contains a slash or an ampersand
    if '/' in input_string:
        # Split the string by the slash
        return input_string.split('/')
    elif '&' in input_string:
        # Split the string by the ampersand, and strip any leading/trailing whitespace
        return [part.strip() for part in input_string.split('&')]
    else:
        # Return an error message if neither delimiter is present
        return input_string

def get_trends(categoriesWatched):
    # Przykładowe dane testowe z wcześniejszego kodu
    categoriesMap = {}
    for category in categoriesWatched:
        categoriesMap[category] = 0

    categoriesWatched = getNewList(categoriesWatched)
    print(categoriesWatched)
    categoriesListTmp = []
    iterator = 1
    print(categoriesWatched)

    # Słownik do przechowywania sum wystąpień dla każdej kategorii
    category_sums = {}

    for category in categoriesWatched:
        if iterator == 5:
            categoriesListTmp.append(category)
            pytrends = TrendReq()
            pytrends.build_payload(categoriesListTmp, geo='', timeframe='now 7-d', gprop='youtube')
            interest_over_time_df = pytrends.interest_over_time()

            # Sumowanie wystąpień dla każdej kategorii
            for col in interest_over_time_df.columns[:-1]:  # Pomijamy kolumnę 'isPartial'
                category_sums[col] = category_sums.get(col, 0) + interest_over_time_df[col].sum()

            iterator = 1
            categoriesListTmp = []
        else:
            categoriesListTmp.append(category)
            iterator += 1

    # Obsługa pozostałych kategorii, jeśli iterator nie wynosi 1
    if iterator != 1:
        pytrends = TrendReq()
        pytrends.build_payload(categoriesListTmp, geo='', timeframe='now 1-d', gprop='youtube')
        interest_over_time_df = pytrends.interest_over_time()

        # Sumowanie wystąpień dla każdej kategorii
        for col in interest_over_time_df.columns[:-1]:  # Pomijamy kolumnę 'isPartial'
            category_sums[col] = category_sums.get(col, 0) + interest_over_time_df[col].sum()

    # Wyświetlanie sum wystąpień dla każdej kategorii
    print(category_sums)
    print(category_sums["Music"])

    categoriesDic = {}
    sumWatched = 0
    for key in category_sums.keys():
        sumWatched += category_sums[key]
    print(sumWatched)

    for category in category_sums.keys():
        for actualCategory in categoriesMap.keys():
            if str(actualCategory).__contains__(category):
                categoriesMap[actualCategory] += category_sums[category]
    print(categoriesMap)

    for key in categoriesMap.keys():
        categoriesMap[key] = (categoriesMap[key] / sumWatched) * 100

    print(categoriesMap)
    return categoriesMap


