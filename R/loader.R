#' Функция для проверки
#'
#' Функция для проверки
#' @export
say_hello <- function() {
  print("HELLO FROM waframium")
}


#' Функция показада начала и конца диапазона с пациентами, хуй знает зачем, я учюсь кароч
#'
#' Функция показада начала и конца диапазона с пациентами, хуй знает зачем, я учюсь кароч
#' @export
visit_subjects_dates <- function(df, subjects = "system_patient_id", dates = "visit_time",  format_ = '%Y.%m.%d') {

  df <- df %>%
    select(subjects = !!sym(subjects), dates = !!sym(dates)) %>%
    arrange(dates)

  min_d <- format(df[1, 2] , format = format_)
  min_s <- df[1,1]
  max_d <- format(df[nrow(df), 2] , format = format_)
  max_s <- df[nrow(df), 1]

  return(paste0("c ", min_d, " [#", min_s, "] по ", max_d, " [#", max_s, "]"))
}
