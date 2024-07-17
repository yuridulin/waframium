#' Функция для проверки
#'
#' Функция для проверки
#' @export
say_hello <- function() {
  print("HELLO FROM waframium")
}

#' Функция для загрузки данных
#'
#' Функция для загрузки данных
#' @export
load_project <- function () {
  projects <- reticulate::import_from_path("./python/projects.py")
  loader <- reticulate::import_from_path("./python/loader.py")

  dynamic <-loader$loadDynamic(P_22EF02, include_dead=False)
}
