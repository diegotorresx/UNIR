
def ingresar_calificaciones():
    boolInputCourses : bool = True
    listCoursesNames : list[str] = []
    listCalificationCourses : list[float] = []
    while boolInputCourses :
      strCourseName : str = input("Ingresa el nombre de la asignatura: ")
      intCourseCalification : float = float(input("Ingresa la calificació del curso: "))
      listCoursesNames.append(strCourseName)
      listCalificationCourses.append(intCourseCalification)
      intNewCourse : int = int(input("Ingresa 1 si deseas agregar una nueva materia. Ingresa 0 si no deseas agregar más materias: "))
      if (intNewCourse == 1):
        boolInputCourses = True
      else:
        boolInputCourses = False
        
    print(listCoursesNames)
    print(listCalificationCourses)
    return(listCoursesNames,listCalificationCourses)
  
def determinar_estado(calificaciones,umbral):
  listPasedCourses : list[int] = []
  listFailedCourses : list [int] = []
  for calificacion in calificaciones:
      if (calificacion < umbral):
        listFailedCourses.append(calificaciones.index(calificacion))
      else:
        listPasedCourses.append(calificaciones.index(calificacion))
  print(listFailedCourses)
  print(listPasedCourses)
  return (listPasedCourses,listFailedCourses)

getCoursesCalification = ingresar_calificaciones()
getCoursesStatus = determinar_estado(getCoursesCalification[1], 5.0)
print("Cursos Aprobados: {getCoursesStatus.listPasedCourses}")
print("Cursos Reprobados: {getCoursesStatus.listFailedCourses}")