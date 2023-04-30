import re
import time

from playwright.sync_api import Page
from sqlalchemy import create_engine, text

from src.database import _get_url


def delete_user():
    engine = create_engine(_get_url(async_=False))
    with engine.connect() as connection:
        user_id = connection.execute(
            text("SELECT id FROM public.users WHERE email = 'test';")
        ).first()
        user_id = user_id[0] if user_id else None
        if user_id:
            connection.execute(
                text(f"DELETE FROM public.operations WHERE user_id = {user_id};")
            )
            connection.execute(text("DELETE FROM public.users WHERE email = 'test';"))
            connection.commit()


def login(page):
    page.get_by_role("button", name="Sign In").click()
    page.get_by_placeholder("email").fill("test")
    page.get_by_placeholder("password").click()
    page.get_by_placeholder("password").fill("test")
    page.get_by_role("button", name="Login").click()


def test_auth(page: Page) -> None:
    delete_user()
    page.goto("http://127.0.0.1:3000/")
    page.get_by_role("button", name="Sign Up").click()
    page.get_by_placeholder("email").fill("test")
    page.get_by_placeholder("password", exact=True).click()
    page.get_by_placeholder("password", exact=True).fill("test")
    page.get_by_placeholder("confirm password").click()
    page.get_by_placeholder("confirm password").fill("test")
    page.get_by_role("button", name="Register").click()
    login(page)
    assert page.get_by_role("button", name="Додати").is_enabled()


def test_add_operation(page: Page) -> None:
    page.goto("http://127.0.0.1:3000/")
    login(page)
    page.get_by_role("button", name="Додати").click()
    page.get_by_placeholder("сума").fill("100")
    page.get_by_placeholder("опис").fill("test")
    page.locator("svg").click()
    time.sleep(0.3)
    page.get_by_text("Ветеринарні послуги", exact=True).last.click()
    page.get_by_role("button", name="Додати").click()
    time.sleep(0.3)
    assert (
        page.get_by_text(
            re.compile("-100 ₴testВетеринарні послугиручний спосіб")
        ).count()
        > 0
    )


def test_add_old_operation(page: Page) -> None:
    page.goto("http://127.0.0.1:3000/")
    login(page)
    page.get_by_role("button", name="Додати").click()
    page.get_by_placeholder("сума").fill("100")
    page.get_by_placeholder("опис").fill("test")
    page.get_by_placeholder("час").fill("2023-04-25T05:15")
    page.locator("svg").click()
    time.sleep(0.3)
    page.get_by_text("Продукти", exact=True).click()
    page.get_by_role("button", name="Додати").click()
    page.get_by_placeholder("dashboard-time").fill("2023-04-25")
    assert page.get_by_text("-100 ₴testПродуктиручний спосіб05:15").count() == 1
