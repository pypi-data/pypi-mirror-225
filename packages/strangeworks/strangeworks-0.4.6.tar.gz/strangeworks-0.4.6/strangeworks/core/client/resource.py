"""resources.py."""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from strangeworks.core.client.platform import API, Operation


@dataclass
class Product:
    """Represents a Platform Product object."""

    slug: str
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        """Create a Product object from Dictionary."""
        return Product(
            slug=d.get("slug"),
            name=d.get("name"),
        )


@dataclass
class Resource:
    """Represents a Platform Resource object."""

    slug: str
    product: Product
    name: Optional[str] = None
    status: Optional[str] = None
    is_deleted: Optional[bool] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        """Generate a Resource object from a dictionary.

        Parameters
        ----------
        cls
            Class object.
        d: Dict
            Resource object attributes represented as a dictionary.

        Return
        ------
        An intance of the Resource object.
        """
        return Resource(
            slug=d.get("slug"),
            status=d.get("status"),
            name=d.get("name"),
            product=Product.from_dict(d.get("product")),
            is_deleted=d.get("isDeleted"),
        )

    def proxy_url(self, path: Optional[str] = None) -> str:
        """Return the proxy URL for the resource.

        Parameters
        ----------
        path: str | None
            additional path that denotes a service/product endpoint.

        Returns
        ------
        str:
           url that the proxy will use to make calls to the resource.
        """
        if path is None:
            return f"/products/{self.product.slug}/resource/{self.slug}"

        return f"/products/{self.product.slug}/resource/{self.slug}/{path.strip('/')}"


_get_op = Operation(
    query="""
        query sdk_get_resources {
            workspace  {
                resources {
                    edges {
                        node {
                            slug
                            isDeleted
                            status
                            product {
                                slug
                                name
                            }
                        }
                    }
                }
            }
        }
    """
)


def get(
    client: API,
    resource_slug: Optional[str] = None,
) -> Optional[List[Resource]]:
    """Retrieve a list of available resources.

    Parameters
    ----------
    resource_slug: Optional[str]
        If supplied, only the resource whose slug matches will be returned. Defaults to
        None.

    Return
    ------
    Optional[List[Resource]]
        List of resources or None if workspace has no resources configured.
    """
    workspace = client.execute(_get_op).get("workspace")
    raw_list = workspace.get("resources")
    resources = (
        list(map(lambda x: Resource.from_dict(x.get("node")), raw_list.get("edges")))
        if raw_list
        else None
    )
    if resource_slug and resources:
        resources = [res for res in resources if res.slug == resource_slug]
    return resources
