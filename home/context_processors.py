from .models import Profile


def profile(request):
    """
    Makes `profile` available in every template automatically —
    navbar, footer, and any page that needs it, without every
    view remembering to fetch it manually.

    Assumes a single-row Profile model (one professor, one site).
    If this ever needs to support multiple profiles, this is the
    first place that breaks — flag it if that's a future possibility.
    """
    return {'profile': Profile.objects.first()}