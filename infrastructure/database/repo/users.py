from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        id: int,
        full_name: str,
        username: str | None = None,
    ) -> User:
        """
        Creates or updates a new user in the database and returns the user object.
        """
        insert_stmt = (
            insert(User)
            .values(
                id=id,
                username=username,
                full_name=full_name,
            )
            .on_conflict_do_update(
                index_elements=[User.id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()
