from typing import Optional, List, Tuple, Literal
from unlok.funcs import execute, aexecute
from pydantic import BaseModel, Field
from rath.scalars import ID
from enum import Enum
from unlok.rath import UnlokRath


class ApplicationClientType(str, Enum):
    """An enumeration."""

    CONFIDENTIAL = "CONFIDENTIAL"
    "Confidential"
    PUBLIC = "PUBLIC"
    "Public"


class ApplicationAuthorizationGrantType(str, Enum):
    """An enumeration."""

    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"
    "Authorization code"
    IMPLICIT = "IMPLICIT"
    "Implicit"
    PASSWORD = "PASSWORD"
    "Resource owner password-based"
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    "Client credentials"
    OPENID_HYBRID = "OPENID_HYBRID"
    "OpenID connect hybrid"


class ApplicationAlgorithm(str, Enum):
    """An enumeration."""

    A_ = "A_"
    "No OIDC support"
    RS256 = "RS256"
    "RSA with SHA-2 256"
    HS256 = "HS256"
    "HMAC with SHA-2 256"


class ClientKind(str, Enum):
    """An enumeration."""

    WEBSITE = "WEBSITE"
    "Website"
    DESKTOP = "DESKTOP"
    "Dekstop"
    USER = "USER"
    "User"


class FilterMethod(str, Enum):
    HOST_REGEX = "HOST_REGEX"
    HOST_IS = "HOST_IS"
    HOST_IS_NOT = "HOST_IS_NOT"
    PORT_IS = "PORT_IS"
    PORT_IS_NOT = "PORT_IS_NOT"
    VERSION_IS = "VERSION_IS"
    VERSION_IS_NOT = "VERSION_IS_NOT"
    VERSION_REGEX = "VERSION_REGEX"
    IDENTIFIER_IS = "IDENTIFIER_IS"
    IDENTIFIER_IS_NOT = "IDENTIFIER_IS_NOT"
    IDENTIFIER_REGEX = "IDENTIFIER_REGEX"
    USER_IS = "USER_IS"
    USER_IS_DEVELOPER = "USER_IS_DEVELOPER"


class GrantType(str, Enum):
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    IMPLICIT = "IMPLICIT"
    PASSWORD = "PASSWORD"
    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"


class PublicFaktType(str, Enum):
    DEKSTOP = "DEKSTOP"
    WEBSITE = "WEBSITE"


class FilterInput(BaseModel):
    method: FilterMethod
    value: str

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ScopeFragment(BaseModel):
    typename: Optional[Literal["Scope"]] = Field(alias="__typename", exclude=True)
    value: str
    label: str
    description: Optional[str]

    class Config:
        frozen = True


class UserFragmentProfile(BaseModel):
    typename: Optional[Literal["Profile"]] = Field(alias="__typename", exclude=True)
    avatar: Optional[str]

    class Config:
        frozen = True


class UserFragment(BaseModel):
    typename: Optional[Literal["HerreUser"]] = Field(alias="__typename", exclude=True)
    id: ID
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    email: str
    profile: Optional[UserFragmentProfile]

    class Config:
        frozen = True


class CreateChannelMutationCreatechannel(BaseModel):
    typename: Optional[Literal["Channel"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: Optional[str]
    token: Optional[str]

    class Config:
        frozen = True


class CreateChannelMutation(BaseModel):
    create_channel: Optional[CreateChannelMutationCreatechannel] = Field(
        alias="createChannel"
    )

    class Arguments(BaseModel):
        name: str
        token: str

    class Meta:
        document = "mutation CreateChannel($name: String!, $token: String!) {\n  createChannel(name: $name, token: $token) {\n    id\n    name\n    token\n  }\n}"


class PublishToChannelMutationPublishtochannelChannel(BaseModel):
    typename: Optional[Literal["Channel"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: Optional[str]
    token: Optional[str]

    class Config:
        frozen = True


class PublishToChannelMutationPublishtochannel(BaseModel):
    typename: Optional[Literal["PublishResult"]] = Field(
        alias="__typename", exclude=True
    )
    status: Optional[str]
    channel: Optional[PublishToChannelMutationPublishtochannelChannel]

    class Config:
        frozen = True


class PublishToChannelMutation(BaseModel):
    publish_to_channel: Optional[PublishToChannelMutationPublishtochannel] = Field(
        alias="publishToChannel"
    )

    class Arguments(BaseModel):
        channel: ID
        message: str
        title: str

    class Meta:
        document = "mutation PublishToChannel($channel: ID!, $message: String!, $title: String!) {\n  publishToChannel(channel: $channel, message: $message, title: $title) {\n    status\n    channel {\n      id\n      name\n      token\n    }\n  }\n}"


class NotifyUserMutationNotifyuserChannel(BaseModel):
    typename: Optional[Literal["Channel"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: Optional[str]
    token: Optional[str]

    class Config:
        frozen = True


class NotifyUserMutationNotifyuser(BaseModel):
    typename: Optional[Literal["PublishResult"]] = Field(
        alias="__typename", exclude=True
    )
    status: Optional[str]
    channel: Optional[NotifyUserMutationNotifyuserChannel]

    class Config:
        frozen = True


class NotifyUserMutation(BaseModel):
    notify_user: Optional[Tuple[Optional[NotifyUserMutationNotifyuser], ...]] = Field(
        alias="notifyUser"
    )

    class Arguments(BaseModel):
        user: ID
        message: str
        title: str

    class Meta:
        document = "mutation NotifyUser($user: ID!, $message: String!, $title: String!) {\n  notifyUser(user: $user, message: $message, title: $title) {\n    status\n    channel {\n      id\n      name\n      token\n    }\n  }\n}"


class Get_scopesQuery(BaseModel):
    scopes: Optional[Tuple[Optional[ScopeFragment], ...]]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment Scope on Scope {\n  value\n  label\n  description\n}\n\nquery get_scopes {\n  scopes {\n    ...Scope\n  }\n}"


class Aget_scopeQuery(BaseModel):
    scope: Optional[ScopeFragment]

    class Arguments(BaseModel):
        id: str

    class Meta:
        document = "fragment Scope on Scope {\n  value\n  label\n  description\n}\n\nquery aget_scope($id: String!) {\n  scope(key: $id) {\n    ...Scope\n  }\n}"


class Search_scopesQueryOptions(BaseModel):
    typename: Optional[Literal["Scope"]] = Field(alias="__typename", exclude=True)
    value: str
    label: str

    class Config:
        frozen = True


class Search_scopesQuery(BaseModel):
    options: Optional[Tuple[Optional[Search_scopesQueryOptions], ...]]

    class Arguments(BaseModel):
        search: Optional[str]
        values: Optional[List[Optional[ID]]]

    class Meta:
        document = "query search_scopes($search: String, $values: [ID]) {\n  options: scopes(search: $search, values: $values) {\n    value\n    label\n  }\n}"


class MeQuery(BaseModel):
    me: Optional[UserFragment]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment User on HerreUser {\n  id\n  username\n  email\n  profile {\n    avatar\n  }\n}\n\nquery me {\n  me {\n    ...User\n  }\n}"


async def acreate_channel(
    name: str, token: str, rath: UnlokRath = None
) -> Optional[CreateChannelMutationCreatechannel]:
    """CreateChannel



    Arguments:
        name (str): name
        token (str): token
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[CreateChannelMutationCreatechannel]"""
    return (
        await aexecute(CreateChannelMutation, {"name": name, "token": token}, rath=rath)
    ).create_channel


def create_channel(
    name: str, token: str, rath: UnlokRath = None
) -> Optional[CreateChannelMutationCreatechannel]:
    """CreateChannel



    Arguments:
        name (str): name
        token (str): token
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[CreateChannelMutationCreatechannel]"""
    return execute(
        CreateChannelMutation, {"name": name, "token": token}, rath=rath
    ).create_channel


async def apublish_to_channel(
    channel: ID, message: str, title: str, rath: UnlokRath = None
) -> Optional[PublishToChannelMutationPublishtochannel]:
    """PublishToChannel



    Arguments:
        channel (ID): channel
        message (str): message
        title (str): title
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[PublishToChannelMutationPublishtochannel]"""
    return (
        await aexecute(
            PublishToChannelMutation,
            {"channel": channel, "message": message, "title": title},
            rath=rath,
        )
    ).publish_to_channel


def publish_to_channel(
    channel: ID, message: str, title: str, rath: UnlokRath = None
) -> Optional[PublishToChannelMutationPublishtochannel]:
    """PublishToChannel



    Arguments:
        channel (ID): channel
        message (str): message
        title (str): title
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[PublishToChannelMutationPublishtochannel]"""
    return execute(
        PublishToChannelMutation,
        {"channel": channel, "message": message, "title": title},
        rath=rath,
    ).publish_to_channel


async def anotify_user(
    user: ID, message: str, title: str, rath: UnlokRath = None
) -> Optional[List[Optional[NotifyUserMutationNotifyuser]]]:
    """NotifyUser



    Arguments:
        user (ID): user
        message (str): message
        title (str): title
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[NotifyUserMutationNotifyuser]]]"""
    return (
        await aexecute(
            NotifyUserMutation,
            {"user": user, "message": message, "title": title},
            rath=rath,
        )
    ).notify_user


def notify_user(
    user: ID, message: str, title: str, rath: UnlokRath = None
) -> Optional[List[Optional[NotifyUserMutationNotifyuser]]]:
    """NotifyUser



    Arguments:
        user (ID): user
        message (str): message
        title (str): title
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[NotifyUserMutationNotifyuser]]]"""
    return execute(
        NotifyUserMutation,
        {"user": user, "message": message, "title": title},
        rath=rath,
    ).notify_user


async def aget_scopes(
    rath: UnlokRath = None,
) -> Optional[List[Optional[ScopeFragment]]]:
    """get_scopes



    Arguments:
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ScopeFragment]]]"""
    return (await aexecute(Get_scopesQuery, {}, rath=rath)).scopes


def get_scopes(rath: UnlokRath = None) -> Optional[List[Optional[ScopeFragment]]]:
    """get_scopes



    Arguments:
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ScopeFragment]]]"""
    return execute(Get_scopesQuery, {}, rath=rath).scopes


async def aaget_scope(id: str, rath: UnlokRath = None) -> Optional[ScopeFragment]:
    """aget_scope



    Arguments:
        id (str): id
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[ScopeFragment]"""
    return (await aexecute(Aget_scopeQuery, {"id": id}, rath=rath)).scope


def aget_scope(id: str, rath: UnlokRath = None) -> Optional[ScopeFragment]:
    """aget_scope



    Arguments:
        id (str): id
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[ScopeFragment]"""
    return execute(Aget_scopeQuery, {"id": id}, rath=rath).scope


async def asearch_scopes(
    search: Optional[str] = None,
    values: Optional[List[Optional[ID]]] = None,
    rath: UnlokRath = None,
) -> Optional[List[Optional[Search_scopesQueryOptions]]]:
    """search_scopes



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[Optional[ID]]], optional): values.
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[Search_scopesQueryScopes]]]"""
    return (
        await aexecute(
            Search_scopesQuery, {"search": search, "values": values}, rath=rath
        )
    ).scopes


def search_scopes(
    search: Optional[str] = None,
    values: Optional[List[Optional[ID]]] = None,
    rath: UnlokRath = None,
) -> Optional[List[Optional[Search_scopesQueryOptions]]]:
    """search_scopes



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[Optional[ID]]], optional): values.
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[Search_scopesQueryScopes]]]"""
    return execute(
        Search_scopesQuery, {"search": search, "values": values}, rath=rath
    ).scopes


async def ame(rath: UnlokRath = None) -> Optional[UserFragment]:
    """me



    Arguments:
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[UserFragment]"""
    return (await aexecute(MeQuery, {}, rath=rath)).me


def me(rath: UnlokRath = None) -> Optional[UserFragment]:
    """me



    Arguments:
        rath (unlok.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[UserFragment]"""
    return execute(MeQuery, {}, rath=rath).me
