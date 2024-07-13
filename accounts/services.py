from .models import Relation, User


class RelationService:
    @staticmethod
    def follow(from_user: User, to_user: User):
        if not Relation.objects.filter(from_user=from_user, to_user=to_user).exists():
            Relation.objects.create(from_user=from_user, to_user=to_user)
            from_user.followings_count += 1
            to_user.followers_count += 1
            from_user.save()
            to_user.save()
            return True
        return False

    @staticmethod
    def unfollow(from_user: User, to_user: User):
        relation = Relation.objects.filter(from_user=from_user, to_user=to_user)
        if relation.exists():
            relation.delete()
            from_user.followings_count -= 1
            to_user.followers_count -= 1
            from_user.save()
            to_user.save()
            return True
        return False


class RelationFactory:
    @staticmethod
    def get_action(action):
        if action == "follow":
            return RelationService.follow
        elif action == "unfollow":
            return RelationService.unfollow
        else:
            raise ValueError("Invalid action")
