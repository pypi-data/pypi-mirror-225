"""
Small API for openiris.io using Python Requests.
Downstream flow only, no support for create and
update operations for the time being.

Author: Sotiris Papadiamantis
"""
import requests
from .utilities import data_from_raw
import pandas as pd


def getBookings(cookies, start="2013-03-07", end="2024-03-07"):
    """
    Downloads all bookings linked to a specific cookie

    Args:
        cookies: cookie used for the request
        start: start date to filter results
        end: end date to filter results

    Returns:
        Dataframe of all bookings between start and end dates
    """

    # Set up request url
    url = "https://openiris.io/resourcesAdminBookings/query"

    # Get response
    data_raw = requests.post(url, params={"groupid":"","from": start, "to": end,"userId":"","providerId":""}, cookies=cookies)
    print(data_raw)
    # Return formatted data
    return data_from_raw(data_raw.content, data_field="Data")


def getGroupIDs(cookies):
    """
    Downloads a list of all group ids linked to an account

    Args:
        cookies: cookie used for the request

    Returns:
        list of all group ids linked to an account via cookie
    """

    # Set up request url
    url = "https://iris.science-it.ch/groups/query"

    # Get response
    data_raw = requests.post(url, cookies=cookies)

    # Return request content
    return data_from_raw(data_raw.content, data_field="Data")


def getProviderIDs(cookies):
    """
    Downloads a list of all provider ids linked to an account
    Note that you have to activate the Billing option for this
    function to work

    Args:
        cookies: cookie used for the request

    Returns:
        list of all provider ids linked to an account via cookie
    """

    # Set up request url
    url = "https://openiris.io/billingTemplates/queryProviders"

    # Make request
    data_raw = requests.post(url, cookies=cookies)

    # Return formatted data
    return data_from_raw(data_raw.content)


def getUsers(cookies, start="2021-03-07", end="2023-03-08", to_csv=False):
    """
    Downloads a dataframe with information on all users that are
    administered by the account linked to the cookie

    Args:
        cookies: cookie used for the request
        start: start date to filter results
        end: end date to filter results
        to_csv: flag to save dataframe in csv form

    Returns:
        data: dataframe of all users
    """

    # Set up request url
    url = "https://openiris.io/admin-users"

    # Get a list of all provider IDs
    providerIds = getProviderIDs(cookies)

    # Initiate list of providers
    # providerList = []

    # Initiate list of result dataframes
    df_list = []

    # For each provider
    for i in providerIds["Id"]:

        # Perform request
        data_raw = requests.post(
            url, params={"from": start, "to": end, "providerID": i}, cookies=cookies
        )

        # Format data
        data = data_from_raw(data_raw.content, "Data")

        # Append to list of dataframes
        df_list.append(data)

    # Concatenate dataframes
    data = pd.concat(df_list)

    # If store to csv flag
    if to_csv:
        # Store to file
        data.to_csv("users.csv")

    # Return dataframe
    return data


def getResourcesForProvider(cookies, providerId):
    """
    Downloads a dataframe with information on all resources that are
    administered by a specific provider

    Args:
        cookies: cookie used for the request
        providerId: ID of the provider whose resources we will download

    Returns:
        data: dataframe of all resources in provider with providerId
    """

    # Set up request url
    url = "https://openiris.io/admin-users/resources"

    # Perform the request
    raw_data = requests.post(url, params={"providerID": providerId}, cookies=cookies)

    # Return formatted data
    return data_from_raw(raw_data.content, data_field="Data")


def getAllResources(cookies, to_csv=False):
    """
    Downloads a dataframe with information on all resources that are
    administered the account in any provider. This function calls
    the getProviders function and therefore the billing option has
    to be activated

    Args:
        cookies: cookie used for the request
        to_csv: flag to save dataframe in csv form

    Returns:
        df: dataframe of all resources
    """

    # Get a list of all provider IDs
    providerIds = getProviderIDs(cookies)

    # Initiate list of result dataframes
    df_list = []

    for i in providerIds["Id"]:

        # Append result to list
        df_list.append(getResourcesForProvider(cookies, providerId=i))

    # Concatenate results
    data = pd.concat(df_list)

    # If flag save in csv form
    if to_csv:
        data.to_csv("resources.csv")

    return data


def listResourceIDs(cookies):
    """
    Create a list of the IDs of all resources in any
    provider that you might administer

    Args:
        cookies: cookie used for the request

    Returns:
        list of the IDs of all resources in any
    provider that you might administer
    """

    # Request all resources dataframe and cast Resource id
    # column to list
    return getAllResources(cookies)["ResourceId"].tolist()


def getResourceStatistics(cookies, resources, start="2021-03-07", end="2022-03-07"):
    """
    Download all resource usage statistics from Statistics
    page

    Args:
        cookies: cookie used for the request
        resources: list of resources to include in request
        start: start date to filter results
        end: end date to filter results

    Returns:
        Dataframe of statistics table
    """

    # If resources is empty
    if not resources:

        # Select all resources
        resources = listResourceIDs(cookies)

    # Set up request url
    url = "https://openiris.io/statistics/queryResourcesUtilization"

    # Get data in raw form
    raw_data = requests.post(
        url,
        params={
            "resources": resources,
            "from": start,
            "to": end,
            "timeInterval": 1,
            "mode": 1,
        },
        cookies=cookies,
    )

    # Return formatted data
    return data_from_raw(raw_data.content, data_field=False)


def getHeatmapData(cookies, resources, start="2021-03-07", end="2022-03-07"):
    """
    Download all resource usage statistics from Statistics
    page in heatmap from

    Args:
        cookies: cookie used for the request
        resources: list of resources to include in request
        start: start date to filter results
        end: end date to filter results

    Returns:
        Dataframe of statistics table
    """

    # If resources is empty
    if not resources:

        # Select all resources
        resources = listResourceIDs(cookies)

    # Set up request url
    url = "https://openiris.io/statistics/queryHeatmapData"

    # Get data in raw form
    raw_data = requests.post(
        url, params={"resources": resources, "from": start, "to": end}, cookies=cookies
    )

    # Return formatted data
    return data_from_raw(raw_data.content, data_field=False)


def getTotalsReportData(
    cookies, resources, start="2021-03-07", end="2022-03-07", mode="user"
):
    """
    Download all resource usage statistics from Statistics
    page using the usage total option

    Args:
        cookies: cookie used for the request
        resources: list of resources to include in request
        start: start date to filter results
        end: end date to filter results

    Returns:
        Dataframe of statistics table
    """

    # If resources is empty
    if not resources:

        # Select all resources
        resources = listResourceIDs(cookies)

    # Set up request url
    url = "https://openiris.io/statistics/queryTotalsReportData"

    # Get data in raw form
    raw_data = requests.post(
        url,
        params={"resources": resources, "from": start, "to": end, "mode": mode},
        cookies=cookies,
    )

    # Return formatted data
    return data_from_raw(raw_data.content, data_field="OrganizationItems")


def getResourceUsageByUser(
    cookies, resources, start="2021-03-07", end="2022-03-07", mode="scheduled"
):
    """
    Download resource usage by user statistics from Statistics
    page

    Args:
        cookies: cookie used for the request
        resources: list of resources to include in request
        start: start date to filter results
        end: end date to filter results
        mode: query mode parameter

    Returns:
        Dataframe of statistics table
    """

    # If resources is empty
    if not resources:

        # Select all resources
        resources = listResourceIDs(cookies)

    # Set up request url
    url = "https://openiris.io/statistics/queryResourceUsageByUser"

    # Get data in raw form
    raw_data = requests.post(
        url,
        params={"resources": resources, "from": start, "to": end, "mode": mode},
        cookies=cookies,
    )
    return data_from_raw(raw_data.content, data_field="Items")


def getResourceTypes(cookies, providers):
    """
    Get a dataframe with all resource types that
    appear in resource linked to your providers

    Args:
        cookies: cookie used for the request
        providers: list of providers to include in request

    Returns:
        Dataframe of statistics table
    """

    # If resources list is empty
    if not providers:

        # Select all resources
        providers = getProviderIDs(cookies)

    # Set up request url
    url = "https://openiris.io/adminresourcetypes/queryadminproviders"

    # Get data in raw form
    raw_data = requests.post(url, params={"Providers": providers}, cookies=cookies)

    # Return formatted data
    return data_from_raw(raw_data.content, data_field="ParentTypes")


def getCommunities(cookies):
    """
    Get a dataframe with all community ids

    Args:
        cookies: cookie used for the request

    Returns:
        Dataframe of statistics table
    """

    url = "https://openiris.io/communities/query"

    data_raw = requests.post(url, cookies=cookies)

    return data_from_raw(data_raw.content, data_field="Data")


def getCommunityUsers(cookies, community_id):
    """
    Get a dataframe with all users of community with
    community_id. Note that users that are affiliated via
    group affiliation are not visible here. To get a full
    account of the users you must use getCommunityLinkedGroups
    and then use all then query users for each group


    Args:
        cookies: cookie used for the request
        community_id: community id to search.

    Returns:
        Dataframe of users affiliated to the community
    """

    url = "https://openiris.io/communities/querycommunityusers"

    data_raw = requests.post(url, params={"id": community_id}, cookies=cookies)

    return data_from_raw(data_raw.content, data_field="Data")


def getCommunityLinkedGroups(cookies, community_id):
    """
    Get a dataframe with all groups affiliated with the
    community with community_id.

    Args:
        cookies: cookie used for the request
        community_id: community id to search.

    Returns:
        Dataframe of groups affiliated to the community
    """

    url = "https://openiris.io/communities/queryLinkedGroups"

    data_raw = requests.post(url, params={"id": community_id}, cookies=cookies)

    return data_from_raw(data_raw.content, data_field="Data")


def getAdminUsers(
    cookies,
    providerId,
    groupId="",
    start="2021-03-07 10:30",
    end="2022-03-07 10:30",
    showByGroup=False,
    includeTraining=False,
    includeResourceAccess=False,
    includeProviderAccess=False,
):
    """
    Download a dataframe of all users that you administer according to filters

    Args:
        cookies: cookie used for the request
        start: start date to filter results
        end: end date to filter results
        providerId: the provider concerned
        groupId: group concerned
        showByGroup: pagination selection
        includeTraining: include users that have been trained on your resources
        includeResourceAccess: include users that have access to at least one resource
        includeProviderAccess: include users that have access to your provider

    Returns:
        Dataframe of resources that are visible
    """

    # Set up request url
    url = "https://openiris.io/admin-users?"

    # Get data in raw form
    raw_data = requests.post(
        url,
        params={
            "providerId": providerId,
            "groupId": groupId,
            "from": start,
            "to": end,
            "showByGroup": showByGroup,
            "includeTraining": includeTraining,
            "includeResourceAccess": includeResourceAccess,
            "includeProviderAccess": includeProviderAccess,
        },
        cookies=cookies,
    )

    return data_from_raw(raw_data.content, data_field="Data")


def getDistributionList(
    cookies,
    providerId,
    start="2021-03-07 10:30",
    end="2023-03-07 10:30",
    includeUsers=True,
    includeGroupAdmins=False,
    includeGroupHeads=False,
    includeTrainings=False,
    includeResourceAccess=False,
    includeProviderAccess=False,
):
    """
    Creates a distribution list of all Provider user based on filters
    Note: Group filtering is not currently operational

    Args:
        cookies: cookie used for the request
        start: start date to filter results
        end: end date to filter results
        providerId: the provider concerned
        includeUsers: group concerned
        includeGroupAdmins: pagination selection
        includeGroupHeads: include the group heads
        includeTrainings: include users that have been trained on your resources
        includeResourceAccess: include users that have access to at least one resource
        includeProviderAccess: include users that have access to your provider

    Returns:
        Dataframe of resources that are visible
    """

    # Set up request url
    url = "https://openiris.io/admin-users/distribution"

    groupId = ""
    # Get data in raw form
    raw_data = requests.post(
        url,
        params={
            "providerId": providerId,
            "groupId": groupId,
            "from": start,
            "to": end,
            "includeUsers": includeUsers,
            "includeGroupAdmins": includeGroupAdmins,
            "includeGroupHeads": includeGroupHeads,
            "includeTrainings": includeTrainings,
            "includeResourceAccess": includeResourceAccess,
            "includeProviderAccess": includeProviderAccess,
        },
        cookies=cookies,
    )

    return data_from_raw(raw_data.content, data_field="DistributionList")


def createGroup(cookies,
                name,
                shortName,
                contactEmail,
                organization,
                isADIntegrated="false",
                adGroupName="",
                autoApprove="false",
                groupHead="",
                admins="",
                members="",
                emailsEnabled="false",
                orgTypeId="",
                validate="true",
                ):
    """
      Creates a group

      Args:
          cookies: cookie used for the request
          name: group name
          shortName: group short name,
          contactEmail: contact email for group,
          organization: organization ID to affiliate the group to,
          isADIntegrated: boolean for AD integration
          adGroupName: AD integration group name
          autoApprove: auto approve boolean
          groupHead: group head user ID
          admins: list of administrators
          members: list of members
          emailsEnabled: emails enabled boolean
          orgTypeId: type of organization ID
          validate: validate group boolean

      Returns:
          a json instance with Status:Ok and the newly created Group ID
    """

    # Verify if org id is string or integer
    if not isinstance(organization, str):
        organization = str(organization)

    # Set up request url
    url = "https://openiris.io/groups/create"

    # Get data in raw form
    raw_data = requests.post(
        url,
        params={
            "name": name,
            "shortName": shortName,
            "contactEmail": contactEmail,
            "organization": organization,
            "isADIntegrated": isADIntegrated,
            "adGroupName": adGroupName,
            "autoApprove": autoApprove,
            "groupHead": groupHead,
            "admins": admins,
            "members": members,
            "emailsEnabled": emailsEnabled,
            "orgTypeId": orgTypeId,
            "validate": validate,
        },
        cookies=cookies,
    )




def updateGroup(cookies,
                id,
                name,
                shortName,
                contactEmail,
                organizationName,
                organizationId,
                affiliatedDepartment,
                isADIntegrated="false",
                adGroupName="",
                autoApprove="false",
                groupHead="",
                orgTypeId="",
                allowDifferentOrganizations="false",
                linkUrl="",
                nickname="",
                isOrgAdmin="false",
                isInactive="false",
                isInactiveShowToAdmins="false",
                ):

    """
      Updates a group

      Args:
          cookies: cookie used for the request
          id: id of the group
          name: group name
          shortName: group short name,
          contactEmail: contact email for group,
          organizationName: organization Name,
          organizationId: organization ID,
          affiliatedDepartment: id of affiliated department,
          isADIntegrated: boolean for AD integration
          adGroupName: AD integration group name
          autoApprove: auto approve boolean
          groupHead: group head user ID
          orgTypeId: type of organization ID
          allowDifferentOrganizations: boolean to allow users from outside org
          linkUrl url to group page
          nickname: group nickname string
          isOrgAdmin: is the requester org admin boolean
          isInactive: is the group inactive boolean
          isInactiveShowToAdmins: show to admin if inactive

      Returns:
          a json instance with Status:Ok if successful
    """

    # Set up request url
    url = "https://openiris.io/groups/edit"

    # Get data in raw form
    raw_data = requests.post(
        url,
        params={
            "id": id,
            "name": name,
            "shortName": shortName,
            "contactEmail": contactEmail,
            "organizationName": organizationName,
            "organizationId": organizationId,
            "affiliatedDepartment": affiliatedDepartment,
            "isADIntegrated": isADIntegrated,
            "adGroupName": adGroupName,
            "autoApprove": autoApprove,
            "groupHead": groupHead,
            "orgTypeId": orgTypeId,
            "allowDifferentOrganizations": allowDifferentOrganizations,
            "linkUrl": linkUrl,
            "nickname": nickname,
            "isOrgAdmin": isOrgAdmin,
            "isInactive": isInactive,
            "isInactiveShowToAdmins": isInactiveShowToAdmins,
        },
        cookies=cookies,
    )

    status = data_from_raw(raw_data.content, data_field="Status")
    if status == "OK":
        return True
    else:
        return False


def deleteGroups(cookies, groupId):
    """
    Deletes a group

       Args:
              cookies: cookie used for the request
              groupId: groupId to delete

        Returns:
              a json instance with Status:"OK" if successful
    """

    # Set up request url
    url = "https://openiris.io/groups/delete"

    # Get data in raw form
    raw_data = requests.post(url, params={"groupId": groupId}, cookies=cookies)

    status = data_from_raw(raw_data.content, data_field="Status")
    if status == "OK":
        return True
    else:
        return False


def addAdmin(cookies, groupId, userId):
    """
    Adds admin to a group

       Args:
              cookies: cookie used for the request
              groupId: groupId to delete
              userId: user to add as admin

        Returns:
              a json instance with Status:"OK" if successful
    """

    url = 'https://openiris.io/groups/addadmin'

    raw_data = requests.post(url, params={'groupId': groupId, 'userId': userId}, cookies=cookies)

    return raw_data.content




