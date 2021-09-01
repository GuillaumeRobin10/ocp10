from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .jwtverification import getuser

from .models import Projects, Contributors, Issues, Comments
from .serializers import CreateUserSerializer, UserSerializer
from .serializers import ProjectSerializer, ProjectUpdateSerializer
from .serializers import ContributorSerializer
from .serializers import IssuesSerializer, IssuesPostSerializer, IssuesupdateSerializer
from .serializers import CommentsSerializer, CommentPostSerializer


@api_view(['POST'])
def signup(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', "POST"])
def projet_get_info_or_add_a_new_project(request):
    user = getuser(request)
    if request.method == "GET":
        project_list_for_user = Contributors().get_project_id_list_by_user_id(user.id)
        if project_list_for_user:
            projects_list = Projects().get_project_list_by_list_of_id(project_list_for_user)
            if projects_list:
                serializer = ProjectSerializer(projects_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("this project doesn't exists", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("you don't contribute to a project", status=status.HTTP_403_FORBIDDEN)
    elif request.method == "POST":
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.create(request.data)
            contribution = Contributors.objects.create(
                user_id=user.id,
                project_id=project.id,
                role='Author',
            )
            contribution.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("bad request", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def uniqueprojet(request, pk_projet):
    user = getuser(request)
    project = get_object_or_404(Projects, id=pk_projet)
    if request.method == "GET":
        project_list_id = Contributors.get_project_id_list_by_user_id(user.id)
        if pk_projet in project_list_id:
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Access denied", status=status.HTTP_403_FORBIDDEN)
    elif request.method == "PUT":
        projets_list = Contributors.get_user_author_projet(user.id)
        if pk_projet in projets_list:
            projectserializer = ProjectUpdateSerializer(project, data=request.data)
            if projectserializer.is_valid():
                projectserializer.save()
                return Response(projectserializer.data, status=status.HTTP_200_OK)
            else:
                return Response("bad request", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("access denied", status=status.HTTP_403_FORBIDDEN)
    elif request.method == "DELETE":
        projets_list = Contributors.get_user_author_projet(user.id)
        if pk_projet in projets_list:
            contributorslist = Contributors.get_contributors_of_a_project_by_id(pk_projet)
            issueslist = Issues.get_issues_by_project_id(pk_projet)
            project.delete()
            for issue in issueslist:
                issue.delete()
            for contribution in contributorslist:
                contribution.delete()
            return Response("project deleted successfully", status=status.HTTP_200_OK)
        else:
            return Response("access denied", status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "POST"])
def projetcontributor(request, pk_projet):
    user = getuser(request)
    projet_list_id = Contributors.get_project_id_list_by_user_id(user.id)
    if pk_projet in projet_list_id:
        if request.method == "GET":
            contributor_list = Contributors.get_contributors_id_of_a_project_by_project_id(pk_projet)
            serializer = UserSerializer(User.objects.filter(id__in=contributor_list), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "POST":
            allowed_projects = Contributors.get_user_author_projet(user.id)
            if pk_projet in allowed_projects:
                serializer = ContributorSerializer(data=request.data)
                if serializer.is_valid():
                    contributor_exist = Contributors.get_contributors_unique_link_by_project_and_user_id(
                        project_id=pk_projet,
                        user_id=serializer.data["user_id"])
                    if not contributor_exist:
                        Contributors.objects.create(
                            user_id=serializer.data["user_id"],
                            project_id=pk_projet,
                            role=serializer.data["role"]
                            )
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response("this link already exists", status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Access denied", status=status.HTTP_403_FORBIDDEN)
    else:
        return Response("Access denied", status=status.HTTP_403_FORBIDDEN)


@api_view(["DELETE"])
def deleteuser(request, pk_projet, pk_user):
    user = getuser(request)
    projet_list_id = Contributors.get_user_author_projet(user.id)
    if pk_projet in projet_list_id:
        contributor = Contributors.get_contributors_unique_link_by_project_and_user_id(project_id=pk_projet, user_id=pk_user)
        if contributor:
            if not contributor[0].role == "Author":
                contributor.delete()
                return Response("link delete successfully", status=status.HTTP_200_OK)
            else:
                return Response("you can't delete the author", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("this link doesn't exits", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Access denied", status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "POST"])
def issues(request, pk_projet):
    user = getuser(request)
    projet_list_id = Contributors.get_project_id_list_by_user_id(user.id)
    if pk_projet in projet_list_id:
        if request.method == "POST":
            serializer = IssuesPostSerializer(data=request.data)
            if serializer.is_valid():
                issue = Issues.objects.create(
                    title=serializer.data['title'],
                    desc=serializer.data['desc'],
                    tag=serializer.data['tag'],
                    priority=serializer.data['priority'],
                    status=serializer.data['status'],
                    project_id=pk_projet,
                    author_user_id=user,
                    assignee_user_id=User.objects.get(id=serializer.data['assignee_user_id'])
                )
                issue.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "GET":
            issueslist = Issues.get_issues_by_project_id(pk_projet)
            if issueslist:
                serializer = IssuesSerializer(issueslist, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Issues not find", status=status.HTTP_404_NOT_FOUND)
    else:

        return Response("Access denied", status=status.HTTP_403_FORBIDDEN)


@api_view(["PUT", "DELETE"])
def editissues(request, pk_projet, pk_issues):
    user = getuser(request)
    projet_list_id = Contributors.get_user_author_projet(user.id)
    if pk_projet in projet_list_id:
        if request.method == "DELETE":
            issue = Issues.get_issues_by_project_and_issue_id(pk_projet, pk_issues)
            if issue:
                issue[0].delete()
                return Response("issues deleted", status=status.HTTP_200_OK)
            else:
                return Response("Issues not find", status=status.HTTP_404_NOT_FOUND)

        elif request.method == "PUT":
            issuesserializer = IssuesupdateSerializer(request.data)
            issue = Issues.get_issues_by_project_and_issue_id(pk_projet, pk_issues)
            if issue:
                issue[0].update(issuesserializer.data)
                issue[0].save()
                return Response(issuesserializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Issues not find", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Access denied", status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "POST"])
def comments(request, pk_projet, pk_issues):
    user = getuser(request)
    projet_list_id = Contributors.get_project_id_list_by_user_id(user.id)
    if pk_projet in projet_list_id:
        if request.method == "GET":
            comms = Comments.get_all_comments_of_an_issue(pk_issues)
            if comms:
                serializer = CommentsSerializer(comms, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("No comments find", status=status.HTTP_404_NOT_FOUND)
        elif request.method == "POST":
            serializer = CommentPostSerializer(data=request.data)
            if serializer.is_valid():
                comment = Comments.objects.create(
                    description=serializer.data["description"],
                    author_user_id=user,
                    issue_id=Issues.objects.get(id=pk_issues)
                )
                comment.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Access denied", status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "PUT", "DELETE"])
def editcomments(request, pk_projet, pk_issues, pk_comments):
    user = getuser(request)
    comm = get_object_or_404(Comments, id=pk_comments, issue_id=pk_issues)
    projet_list_id = Contributors.get_project_id_list_by_user_id(user.id)
    if pk_projet in projet_list_id:
        if request.method == "GET":
            serializer = CommentsSerializer(comm)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            if comm.author_user_id.id == user.id:
                comm.delete()
                return Response("Comment deleted successfully", status=status.HTTP_200_OK)
            else:
                return Response("Access denied", status=status.HTTP_403_FORBIDDEN)
        elif request.method == "PUT":
            if comm.author_user_id.id == user.id:
                serializer = CommentPostSerializer(comm, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Access denied", status=status.HTTP_403_FORBIDDEN)
    else:
        return Response("Access denied", status=status.HTTP_403_FORBIDDEN)
