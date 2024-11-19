def appearance(intervals: dict[str, list[int]]) -> int:
    # собираем списки с интервалами уроков, посещений студентов и учителей
    lessons = list(zip(intervals["lesson"][::2], intervals["lesson"][1::2]))
    students = list(zip(intervals["pupil"][::2], intervals["pupil"][1::2]))
    tutors = list(zip(intervals["tutor"][::2], intervals["tutor"][1::2]))

    def find_intersections(lessons: list, students: list, tutors: list) -> list:
        # находим пересечения интервалов
        intersections = []
        for lesson in lessons:
            for student in students:
                for tutor in tutors:
                    # выбираем максимальное и минимальное время соотвественно
                    start = max(lesson[0], student[0], tutor[0])
                    end = min(lesson[1], student[1], tutor[1])
                    if start < end:
                        intersections.append((start, end))

        
        intersections.sort(key=lambda x: x[0])

        combined = []
        # обработка наложения интервалов между учеником и учителем
        for start, end in intersections:
            if not combined or combined[-1][1] < start:
                combined.append((start, end))
            else:
                combined[-1] = (combined[-1][0], max(combined[-1][1], end))
        
        return combined
    
    # получаем готовый список интервалов
    combined = find_intersections(lessons, students, tutors)

    # считаем время в сек
    total_time = sum(end-start for start, end in combined)

    return total_time
    
   