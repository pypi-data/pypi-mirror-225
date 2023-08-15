from urllib import request, error
from time import sleep
import re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from datetime import datetime, timedelta
import os


class JoyreactorStats:

    def __init__(self,
                 account: str,
                 show_progress: bool = True,
                 open_xls: bool = True,
                 quiet: bool = False
                 ):
        """
        Init class
        :param account:
        :type: str
        :param show_progress:
        :type: bool
        :param open_xls:
        :type: bool
        :param quiet:
        :type: bool
        """

        self.account = account
        self.show_progress = show_progress
        self.open_xls = open_xls
        self.quiet = quiet

        self.post_id_template = re.compile('<a title="ссылка на пост" class="link" href="/post/(\\d*)">ссылка</a>')
        self.page_count_template = re.compile(f"<a href='/user/{self.account}/(\\d*)'")
        self.post_title_template = re.compile('<div><h3>([^<]*)</h3>((?:(?!</div>).)*)</div>')
        self.post_date_template = re.compile('data-time="(\d*)"')
        self.post_comments_template = re.compile("title='количество комментариев'>Комментарии (\d*)</a>")
        self.post_rating_template = re.compile('<span class="post_rating"><span>([\-\d\.]*)<')

        self.post_id = list()
        self.post_title = list()
        self.post_text = list()
        self.post_date = list()
        self.post_comments = list()
        self.post_rating = list()
        self.post_url = list()

        self.header = ['id', 'Заголовок', 'Текстовое описание', 'Дата', 'Комментариев', 'Рейтинг', 'Ссылка']

    def work(self) -> None:
        """
        Run main work
        :return: None
        """

        self.print_msg("--------------------")
        start_date = datetime.now()

        self.print_msg(f'Начало: {start_date.strftime("%d.%m.%Y %H:%M")}')

        page_count = self.get_page_count()

        for page in range(1, page_count + 1):
            self.print_progress(page, page_count)
            self.scrap_page(page)

        save_date = datetime.now()
        xls_file = f'joyreactor_{self.account}_{save_date.strftime("%d.%m.%Y_%H-%M")}.xlsx'

        self.print_msg(f'Сохраняем отчёт в excel ({xls_file}) ...')

        self.save_report(xls_file)

        self.print_msg("Отчёт сохранён")

        end_date = datetime.now()

        self.print_msg(f'Окончание: {end_date.strftime("%d.%m.%Y %H:%M")}')

        len_date = end_date - start_date

        self.print_msg(f'Продолжительность: {self._get_len_date_str(len_date)}')

        self.print_msg("--------------------")

        if self.open_xls:
            os.startfile(xls_file)

    def save_report(self, xls_file: str) -> None:
        """
        Save report to xls
        :param xls_file:
        :type xls_file: str
        :return: None
        """

        work_book = Workbook()

        work_sheet = work_book.active

        work_sheet.append(self.header)

        self._insert_column_data(work_sheet, 'A', self.post_id)
        self._insert_column_data(work_sheet, 'B', self.post_title)
        self._insert_column_data(work_sheet, 'C', self.post_text)
        self._insert_column_data(work_sheet, 'D', self.post_date)
        self._insert_column_data(work_sheet, 'E', self.post_comments)
        self._insert_column_data(work_sheet, 'F', self.post_rating)
        last_row = self._insert_column_data(work_sheet, 'G', self.post_url)

        # Оформление
        header_font = Font(bold=True)
        header_align = Alignment(horizontal='center')

        for row in work_sheet['A1:G1']:
            for cell in row:
                cell.font = header_font
                cell.alignment = header_align

        for row in work_sheet['F2:F' + str(last_row)]:
            for cell in row:
                cell.number_format = "0.00"

        for row in work_sheet['G2:G' + str(last_row)]:
            for cell in row:
                cell.hyperlink = cell.value
                cell.style = "Hyperlink"

        date_align = Alignment(horizontal='center')
        for row in work_sheet['D2:D' + str(last_row)]:
            for cell in row:
                cell.alignment = date_align

        border = Side(style='thin', color="000000")
        table_border = Border(top=border, left=border, right=border, bottom=border)

        for row in work_sheet['A1:G' + str(last_row)]:
            for cell in row:
                cell.border = table_border

        work_sheet.column_dimensions['A'].width = 10
        work_sheet.column_dimensions['B'].width = 30
        work_sheet.column_dimensions['C'].width = 43
        work_sheet.column_dimensions['D'].width = 18
        work_sheet.column_dimensions['E'].width = 15
        work_sheet.column_dimensions['F'].width = 9
        work_sheet.column_dimensions['G'].width = 35

        work_book.save(xls_file)

    def get_page_count(self) -> int:
        """
        Получить количество страниц с постами на аккаунте
        :return: int
        """

        first_url = f'https://joyreactor.cc/user/{self.account}'

        html = self.get_site_html(first_url)

        page_count_list = self.page_count_template.findall(html)
        if len(page_count_list) == 0:
            self.print_msg('\t... что-то пошло не так. Похоже неверный аккаунт.')
            exit(2)

        page_count = int(page_count_list[0]) + 1

        if page_count == 0:
            self.print_msg('\t... что-то пошло не так. Похоже неверный аккаунт.')
            exit(2)

        self.print_msg(f'Количество страниц со статьями: {page_count}')

        return page_count

    def scrap_page(self, page: int) -> None:
        """
        Собрать список постов со страницы
        :param page: номер страницы
        :type: int
        :return:
        """

        page_url = f'https://joyreactor.cc/user/{self.account}/{page}'
        html = self.get_site_html(page_url)

        post_id_list = self.post_id_template.findall(html)
        if len(post_id_list) == 0:
            self.print_msg('\t... что-то пошло не так. Похоже неверный аккаунт.')
            exit(2)

        for post_id in reversed(post_id_list):
            if post_id not in self.post_id:
                self.scrap_post(post_id)
                sleep(5)

    def scrap_post(self, post_id: int) -> None:
        """
        Собрать данные со страницы с постом
        :param post_id: id поста
        :return:
        """

        self.post_id.append(post_id)

        post_url = f'https://joyreactor.cc/post/{post_id}'

        self.post_url.append(post_url)

        html = self.get_site_html(post_url)

        post_title_list = self.post_title_template.findall(html)
        if len(post_title_list) == 0:
            self.print_msg('\t... не удалось получить заголовок со страницы')
            self.post_title.append('НЕ УДАЛОСЬ ПОЛУЧИТЬ')
            self.post_text.append('НЕ УДАЛОСЬ ПОЛУЧИТЬ')

            post_title = 'НЕ УДАЛОСЬ ПОЛУЧИТЬ'
        else:
            self.post_title.append(post_title_list[0][0])
            self.post_text.append(post_title_list[0][1])

            post_title = post_title_list[0][0]

        post_date_list = self.post_date_template.findall(html)
        if len(post_date_list) == 0:
            self.print_msg('\t... не удалось получить дату со страницы')
            post_date = 'НЕ УДАЛОСЬ ПОЛУЧИТЬ'
        else:
            post_date = datetime.utcfromtimestamp(int(post_date_list[0])).strftime('%d.%m.%Y %H:%M')

        self.post_date.append(post_date)

        post_comments_list = self.post_comments_template.findall(html)
        if len(post_comments_list) == 0:
            self.print_msg('\t... не удалось получить количество комментариев со страницы')
            self.post_comments.append('НЕ УДАЛОСЬ ПОЛУЧИТЬ')
        else:
            self.post_comments.append(int(post_comments_list[0]))

        post_rating_list = self.post_rating_template.findall(html)
        if len(post_rating_list) == 0:
            self.print_msg('\t... не удалось получить рейтинг со страницы')
            self.post_rating.append('НЕ УДАЛОСЬ ПОЛУЧИТЬ')
            post_rating = 0.0
        else:
            post_rating = float(post_rating_list[0])
            self.post_rating.append(post_rating)

        self.print_msg(f'\t{post_date} {post_title} [{post_rating}]')

    def get_site_html(self, url: str) -> str:
        """
        Получить содержимое страницы в текстовом виде
        :param url: URL страницы
        :type: str
        :return: str
        """

        self.print_msg(f'\t\tGet {url}')

        try:
            response = request.urlopen(url)
        except error.HTTPError as e:
            self.print_msg('... страница недоступна')
            exit(1)

        html = response.read().decode(response.headers.get_content_charset())

        return html

    def print_msg(self, msg: str) -> None:
        """
        Print message
        :param msg:
        :type: str
        :return: None
        """

        if not self.quiet and self.show_progress:
            print(f'{msg}')

    def print_progress(self, cur_page: int, page_count: int) -> None:
        """
        Print progress
        :param cur_page:
        :param page_count:
        :return: None
        """

        self.print_msg(f'[{cur_page}/{page_count}]')

    @staticmethod
    def _insert_column_data(work_sheet, column: str, data, start_row: int = 2) -> int:
        """
        Вставить в excel файл данные одного столбца.
        :param work_sheet:
        :param column:
        :param data:
        :param start_row:
        :return: Последняя вставленная строка
        """
        kolvo = start_row
        for el in data:
            work_sheet[column + str(kolvo)] = el
            kolvo += 1

        return kolvo - 1

    @staticmethod
    def _get_len_date_str(len_date: timedelta) -> str:
        """
        Получить продолжительность работы в текстовом виде
        :param len_date:
        :return:
        """

        seconds = len_date.total_seconds()
        hours = int(seconds / 3600)
        mins = int((seconds - hours * 3600) / 60)
        secs = int(seconds - hours * 3600 - mins * 60)

        result = ''

        if hours > 0:
            result = f'{hours} ч.'
        if mins > 0:
            result = f'{result} {mins} м.'
        if secs > 0:
            result = f'{result} {secs} сек.'

        return result

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, account: str):
        self.__account = account

    @property
    def quiet(self) -> bool:
        return self.__quiet

    @quiet.setter
    def quiet(self, quiet: bool):
        self.__quiet = quiet

    @property
    def show_progress(self) -> bool:
        return self.__show_progress

    @show_progress.setter
    def show_progress(self, show_progress: bool):
        self.__show_progress = show_progress

    @property
    def open_xls(self) -> bool:
        return self.__open_xls

    @open_xls.setter
    def open_xls(self, open_xls: bool):
        self.__open_xls = open_xls
