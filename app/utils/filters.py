from app.utils import blueprint
from statistics import mean


# to format a datetime object
@blueprint.app_template_filter('timestring')
def timestring(timestamp):
    return timestamp.strftime("%m/%d/%Y at %H:%M")


# to get info about single measurements
@blueprint.app_template_filter('category1')
def measurements1(nums):
    if len(nums) != 0:
        nums1 = [x.number for x in nums]
        max_num = max(nums, key=lambda number: number.number)
        min_num = min(nums, key=lambda number: number.number)
        return {'mean': f"{mean(nums1)}",
                'max': max_num,
                'max_time': timestring(max_num.timestamp),
                'min': min_num,
                'min_time': timestring(min_num.timestamp)}


# to get info about double measurements
@blueprint.app_template_filter('category2')
def measurements2(nums):
    if len(nums) != 0:
        uppers = [x.upper_number for x in nums]
        lowers = [x.lower_number for x in nums]
        max_upper = max(nums, key=lambda number: number.upper_number)
        max_lower = max(nums, key=lambda number: number.lower_number)
        min_upper = min(nums, key=lambda number: number.upper_number)
        min_lower = min(nums, key=lambda number: number.lower_number)
        return {'mean': f"{mean(uppers)}/{mean(lowers)}",
                'max_upper': max_upper,
                'max_upper_time': timestring(max_upper.timestamp),
                'max_lower': max_lower,
                'max_lower_time': timestring(max_lower.timestamp),
                'min_upper': min_upper,
                'min_upper_time': timestring(min_upper.timestamp),
                'min_lower': min_lower,
                'min_lower_time': timestring(min_lower.timestamp)}


# to get info about triple measurements
@blueprint.app_template_filter('category3')
def measurements3(nums):
    if len(nums) != 0:
        firsts = [x.first_number for x in nums]
        seconds = [x.second_number for x in nums]
        thirds = [x.third_number for x in nums]
        max_first = max(nums, key=lambda number: number.first_number)
        max_second = max(nums, key=lambda number: number.second_number)
        max_third = max(nums, key=lambda number: number.third_number)
        min_first = min(nums, key=lambda number: number.first_number)
        min_second = min(nums, key=lambda number: number.second_number)
        min_third = min(nums, key=lambda number: number.third_number)
        return {'mean': f"{mean(firsts)}/{mean(seconds)}/{mean(thirds)}",
                'max_first': max_first,
                'max_first_time': timestring(max_first.timestamp),
                'max_second': max_second,
                'max_second_time': timestring(max_second.timestamp),
                'max_third': max_third,
                'max_third_time': timestring(max_third.timestamp),
                'min_first': min_first,
                'min_first_time': timestring(min_first.timestamp),
                'min_second': min_second,
                'min_second_time': timestring(min_second.timestamp),
                'min_third': min_third,
                'min_third_time': timestring(min_third.timestamp)}


