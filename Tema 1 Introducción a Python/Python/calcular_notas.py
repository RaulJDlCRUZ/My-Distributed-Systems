def calc_grades(grades):
    _pass=0
    fail=0
    for grade in grades:
        if grade >= 5:
            _pass += 1
        else:
            fail += 1
    return _pass, fail

grades = [1,2,6,7]
""" _pass=0
fail=0
for grade in grades:
    if grade >= 5:
        _pass += 1
    else:
        fail += 1 """

""" _pass, fail = calc_grades(grades)
print("Aprobados: ",_pass)
print("Reprobados: ",fail) """

if __name__ == "__main__":
    grades = [1,2,6,7]
    _pass, fail = calc_grades(grades)
    print("Aprobados: ",_pass)
    print("Reprobados: ",fail)