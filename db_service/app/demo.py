from sqlalchemy import select
from app.database import SessionLocal
from app.models import User, Post, PostRating

def run_demo():
    with SessionLocal() as db:
        print("=== ДЕМОНСТРАЦИЯ ЛАБОРАТОРНОЙ РАБОТЫ №1 ===")

        # Сценарий: Просмотр ленты подписок для alice
        alice = db.scalar(select(User).where(User.username == "alice"))
        print(f"\nПользователь: {alice.username}")
        print("Подписки:", [u.username for u in alice.following])

        # Получение постов авторов из подписок
        feed_posts = db.scalars(
            select(Post).where(Post.author_id.in_([u.id for u in alice.following]))
        ).all()

        print("\nЛента новостей Alice:")
        for post in feed_posts:
            print(f"- Пост #{post.id} от {post.author.username}: '{post.content}'")

            # Вывод оценок поста
            for rating in post.ratings:
                print(f"  Оценка от {rating.user.username}: {rating.score}/5 (Отзыв: {rating.review_text})")

if __name__ == "__main__":
    run_demo()