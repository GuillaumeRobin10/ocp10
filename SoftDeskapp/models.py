from django.db import models
from django.contrib.auth.models import User


class Projects (models.Model):

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[("back-end", "back-end"),
                                                    ("front-end", "front-end"),
                                                    ("IOS", "IOS"),
                                                    ("Android", "Android")])

    @staticmethod
    def get_project_list_by_list_of_id(list_of_id):
        return Projects.objects.filter(id__in=list_of_id)

    def update(self, dict_of_value):
        keys = dict_of_value.keys()
        for key in keys:
            if key == "title":
                self.title = dict_of_value["title"]
            if key == "description":
                self.description = dict_of_value["description"]
            if key == "type":
                self.type = dict_of_value["type"]


class Contributors(models.Model):

    user_id = models.IntegerField()
    project_id = models.IntegerField()
    role = models.CharField(max_length=255, choices=[("Author", "Author"),
                                                     ("Contributor", "Contributor")])

    @staticmethod
    def get_project_id_list_by_user_id(user_id):
        return [contribution.project_id for contribution in Contributors.objects.filter(user_id=user_id)]

    @staticmethod
    def get_user_author_projet(user_id):
        return [contribution.project_id for contribution in Contributors.objects.filter(user_id=user_id, role="Author")]

    @staticmethod
    def get_contributors_of_a_project_by_id(project_id):
        return Contributors.objects.filter(project_id=project_id)

    @staticmethod
    def get_contributors_unique_link_by_project_and_user_id(project_id, user_id):
        return Contributors.objects.filter(project_id=project_id, user_id=user_id)

    @staticmethod
    def get_contributors_id_of_a_project_by_project_id(project_id):
        return [contributor.user_id for contributor in Contributors.objects.filter(project_id=project_id)]


class Issues(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=1000)
    tag = models.CharField(max_length=100, choices=[("BUG", "BUG"), ("AMÉLIORATION", "AMÉLIORATION"), ("TÂCHE", "TÂCHE")])
    priority = models.CharField(max_length=100, choices=[("FAIBLE", "FAIBLE"), ("MOYENNE", "MOYENNE"), ("ÉLEVÉE", "ÉLEVÉE")])
    project_id = models.IntegerField()
    status = models.CharField(max_length=100, choices=[("À faire", "À faire"), ("En cours", "En cours"), ("Terminé", "Terminé")])
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee")
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_issues_by_project_id(project_id):
        return Issues.objects.filter(project_id=project_id)

    @staticmethod
    def get_issues_by_project_and_issue_id(project_id, issue_id):
        return Issues.objects.filter(id=issue_id, project_id=project_id)

    def update(self, dict_of_value):
        keys = dict_of_value.keys()
        for key in keys:
            if key == "title":
                self.title = dict_of_value["title"]
            if key == "desc":
                self.description = dict_of_value["desc"]
            if key == "tag":
                self.tag = dict_of_value["tag"]
            if key == "priority":
                self.priority = dict_of_value["priority"]
            if key == "status":
                self.status = dict_of_value["status"]


class Comments(models.Model):
    description = models.CharField(max_length=1000)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_all_comments_of_an_issue(issue_id):
        return Comments.objects.filter(issue_id=issue_id)

    @staticmethod
    def get_your_own_comments(identity, user_id):
        return Comments.objects.filter(id=identity, author_user_id=user_id)
