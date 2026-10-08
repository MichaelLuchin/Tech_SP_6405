from app.database import SessionLocal
from app.models import Role, User, UserPassword, Post, Follower, PostRating

def seed_data():
    with SessionLocal() as db:
        # 1. Роли
        admin_role = Role(name="Admin")
        user_role = Role(name="User")
        db.add_all([admin_role, user_role])
        db.commit()

        # 2. Пользователи
        user1 = User(username="alice", role_id=user_role.id)
        user2 = User(username="bob", role_id=user_role.id)
        admin = User(username="admin_user", role_id=admin_role.id)
        db.add_all([user1, user2, admin])
        db.commit()

        # Пароли
        db.add_all([
            UserPassword(user_id=user1.id, password_hash="hash_alice"),
            UserPassword(user_id=user2.id, password_hash="hash_bob"),
            UserPassword(user_id=admin.id, password_hash="hash_admin"),
        ])

        # 3. Подписка (Alice подписывается на Bob)
        user1.following.append(user2)

        # 4. Пост от Bob
        post1 = Post(author_id=user2.id, content="Привет всем! Это мой первый пост в сети.")
        db.add(post1)
        db.commit()

        # 5. Оценка от Alice
        rating = PostRating(user_id=user1.id, post_id=post1.id, score=5, review_text="Крутой пост!")
        db.add(rating)
        db.commit()

        print("Тестовые данные успешно загружены!")

if __name__ == "__main__":
    seed_data()