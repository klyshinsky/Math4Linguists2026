import math


def distance(hotel, x, y):
    dx = hotel['x'] - x
    dy = hotel['y'] - y
    return math.sqrt(dx*dx + dy*dy)


def common_words_count(description, query_words):
    desc_words = description.lower().split()
    count = 0
    for qw in query_words:
        for dw in desc_words:
            if qw == dw:
                count += 1
    return count


def filter_hotels(hotels, max_price, min_rating, category):
    filtered = []
    for h in hotels:
        if h['price'] <= max_price and h['rating'] >= min_rating:
            if category == 0 or h['stars'] == category:
                filtered.append(h)
    return filtered


def sort_hotels_by_distance(hotels, x, y):
    n = len(hotels)
    
    arr = hotels.copy()
    for i in range(n):
        for j in range(0, n - i - 1):
            d1 = distance(arr[j], x, y)
            d2 = distance(arr[j+1], x, y)
            if d1 > d2:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def find_top_hotels(hotels, x, y, max_price, min_rating, category, query_text):
    filtered = filter_hotels(hotels, max_price, min_rating, category)
    query_words = query_text.lower().split()

    candidates = []
    for h in filtered:
        cnt = common_words_count(h['description'], query_words)
        dist = distance(h, x, y)
        candidates.append((cnt, dist, h))
    
    n = len(candidates)
    for i in range(n):
        for j in range(0, n - i - 1):
            cnt1, dist1, _ = candidates[j]
            cnt2, dist2, _ = candidates[j+1]
            if cnt1 < cnt2 or (cnt1 == cnt2 and dist1 > dist2):
                candidates[j], candidates[j+1] = candidates[j+1], candidates[j]
    
    if candidates:
        return candidates[0][2]
    else:
        return None
