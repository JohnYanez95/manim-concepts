"""The base class every concept scene inherits from."""

from manim import Scene, VGroup

from utils.mobjects import header
from utils.theme import BG


class ConceptScene(Scene):
    """A ``Scene`` that already looks like the rest of this repo.

    Two pieces of per-scene boilerplate disappear by inheriting from this:
    setting the background colour, and hand-building a title block. Both were
    repeated verbatim in all four of the original counting-rules scenes, which
    is exactly the kind of copy-paste that lets one scene drift off-palette
    without anyone noticing.

    Subclasses implement ``construct`` as usual. ``title`` returns a mobject
    rather than an animation, so it needs wrapping in one::

        from manim import DOWN, FadeIn

        class MyRule(ConceptScene):
            def construct(self):
                self.play(FadeIn(self.title("My Rule"), shift=0.3 * DOWN))
    """

    def setup(self) -> None:
        """Apply the shared canvas. Manim calls this before ``construct``."""
        super().setup()
        self.camera.background_color = BG

    def title(self, label: str) -> VGroup:
        """Build the title block and remember it as ``self.head``.

        Returns the mobject rather than playing it, so the caller stays in
        control of how it enters::

            self.play(FadeIn(self.title("Combinations"), shift=0.3 * DOWN))
        """
        self.head = header(label)
        return self.head
