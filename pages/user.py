#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.page import Page
from pages.base import Base


class EditProfile(Base):

    _edit_profile_locator = (By.ID, 'edit-profile-link')
    _success_profile_updated = (By.CSS_SELECTOR, '.notice.success p')
    _profile_username_locator = (By.CSS_SELECTOR, 'h1.page-title')
    _stats_section_locator = (By.ID, 'stats')
    _stats_ranking_locator = (By.CSS_SELECTOR, 'section#stats div ul.stats li.ranking')
    _stats_banner_locator = (By.CSS_SELECTOR, 'section#stats div ul.stats li.banners')
    _stats_clicks_locator = (By.CSS_SELECTOR, 'section#stats div ul.stats li.clicks')
    _milestones_section_locator = (By.ID, 'milestones')
    _newsletter_form_locator = (By.ID, 'newsletter-form')


    def click_edit_profile(self):
        self.selenium.find_element(*self._edit_profile_locator).click()
        return self.EditProfileModal(self.testsetup)

    def is_stats_section_visible(self):
        return self.is_element_visible(*self._stats_section_locator)

    @property
    def stats_ranking(self):
        return self.selenium.find_element(*self._stats_ranking_locator).text

    def is_stats_ranking_visible(self):
        return self.is_element_visible(*self._stats_ranking_locator)

    @property
    def stats_banners(self):
        return self.selenium.find_element(*self._stats_banner_locator).text

    def is_stats_banners_visible(self):
        return self.is_element_visible(*self._stats_banner_locator)

    @property
    def stats_clicks(self):
        return self.selenium.find_element(*self._stats_clicks_locator).text

    def is_stats_clicks_visible(self):
        return self.is_element_visible(*self._stats_clicks_locator)

    def is_milestones_section_visible(self):
        return self.is_element_visible(*self._milestones_section_locator)

    def is_newsletter_form_visible(self):
        return self.is_element_visible(*self._newsletter_form_locator)

    @property
    def profile_username(self):
        username_field = self.selenium.find_element(
            *self._profile_username_locator).text
        # strip 'Name: '  from the username field
        parsed_username = username_field[6:]
        return parsed_username

    @property
    def profile_website(self):
        edit_modal = self.click_edit_profile()
        url = edit_modal.website
        edit_modal.click_cancel()
        return url

    def update_profile_name(self, username):
        edit_modal = self.click_edit_profile()
        edit_modal.set_display_name(username)
        edit_modal.click_save_my_changes()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*self._success_profile_updated))

    def update_profile_website(self, url):
        edit_modal = self.click_edit_profile()
        edit_modal.set_website(url)
        edit_modal.click_save_my_changes()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*self._success_profile_updated))

    class EditProfileModal(Page):

        _modal_locator = (By.CSS_SELECTOR, '#profile > div#modal')

        _display_name_label_locator = (By.CSS_SELECTOR, '#modal label[for="id_display_name"]')
        _display_name_locator = (By.CSS_SELECTOR, '#modal input#id_display_name')
        _website_label_locator = (By.CSS_SELECTOR, '#modal label[for="id_website"]')
        _edit_website_locator = (By.CSS_SELECTOR, '#modal input#id_website')
        _save_locator = (By.CSS_SELECTOR, '.button.go')
        _cancel_locator = (By.CSS_SELECTOR, '.button.close')

        def __init__(self, testsetup):
            Page.__init__(self, testsetup)
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: self.is_element_visible(*self._modal_locator))
            self._root_element = self.selenium.find_element(*self._modal_locator)

        @property
        def display_name_label(self):
            return self._root_element.find_element(*self._display_name_label_locator).text

        @property
        def display_name(self):
            return self._root_element.find_element(*self._display_name_locator).get_attribute('value')

        def set_display_name(self, name):
            input_field = self._root_element.find_element(*self._display_name_locator)
            input_field.clear()
            input_field.send_keys(name)

        @property
        def website_label(self):
            return self._root_element.find_element(*self._website_label_locator).text

        @property
        def website(self):
            return str(self._root_element.find_element(*self._edit_website_locator).get_attribute('value'))

        def set_website(self, url):
            input_field = self._root_element.find_element(*self._edit_website_locator)
            input_field.clear()
            input_field.send_keys(url)

        def click_save_my_changes(self):
            self._root_element.find_element(*self._save_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: self.is_element_not_visible(*self._modal_locator))

        def click_cancel(self):
            self._root_element.find_element(*self._cancel_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: self.is_element_not_visible(*self._modal_locator))
