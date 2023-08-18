""" Strucutre Registration

This module is autoimported by arkitekt. It registers the default structure types with the arkitekt
structure-registry so that they can be used in the arkitekt app without having to import them.

You can of course overwrite this in your app if you need to expand to a more complex query.

"""
import logging

logger = logging.getLogger(__name__)


try:
    import rekuest
except ImportError:
    pass
    rekuest = None
    structure_reg = None

# Check if rekuest is installed
# If it is, register the structures with the default structure registry
if rekuest:
    from rekuest.structures.default import (
        get_default_structure_registry,
        Scope,
        id_shrink,
    )
    from rekuest.widgets import SearchWidget
    from mikro_next.api.schema import ImageFragment, aget_image, SearchImagesQuery
    from mikro_next.api.schema import (
        SnapshotFragment,
        aget_snapshot,
        SearchSnapshotsQuery,
    )

    structure_reg = get_default_structure_registry()
    structure_reg.register_as_structure(
        ImageFragment,
        identifier="@mikronext/image",
        aexpand=aget_image,
        ashrink=id_shrink,
        scope=Scope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchImagesQuery.Meta.document, ward="mikro_new"
        ),
    )
    structure_reg.register_as_structure(
        SnapshotFragment,
        identifier="@mikronext/snapshot",
        aexpand=aget_snapshot,
        ashrink=id_shrink,
        scope=Scope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchSnapshotsQuery.Meta.document, ward="mikro_new"
        ),
    )
