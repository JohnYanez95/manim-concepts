"""The base class every concept scene inherits from."""

from manim import Scene, VGroup
from manim.animation.animation import prepare_animation

from utils.mobjects import header
from utils.theme import BG

# The pace every scene's timings are written for, as a fraction of manim's
# native speed. 0.75x turned out to be how these videos are actually watched —
# and slowing a 60 fps file in the player shows each frame for an uneven
# 1/45 s, which is visible judder. Rendering the slower pace natively keeps
# every frame unique and the output at a true 60 fps, so the pace is imposed
# here, once, rather than compensated for in every scene's run_times.
PLAYBACK_SPEED = 0.75


class ConceptScene(Scene):
    """A ``Scene`` that already looks like the rest of this repo.

    Two pieces of per-scene boilerplate disappear by inheriting from this:
    setting the background colour, and hand-building a title block. Both were
    repeated verbatim in all four of the original counting-rules scenes, which
    is exactly the kind of copy-paste that lets one scene drift off-palette
    without anyone noticing.

    Timing is also normalised here: every ``play`` and ``wait`` is stretched
    by ``1 / PLAYBACK_SPEED``, so concept modules keep writing run_times
    against manim's familiar defaults and the rendered output plays at the
    repo's native pace.

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

    def play(self, *animations, **kwargs):
        """Play at the repo's native pace.

        A ``run_time`` passed to ``play`` overrides every animation's own, so
        scaling it covers that case outright. Otherwise each animation carries
        its own timing and is stretched individually — including composites:
        ``AnimationGroup.interpolate`` maps its progress through
        ``max_end_time``, so a scaled group slows its children and lag
        uniformly rather than finishing early.

        ``wait`` is deliberately *not* overridden: ``Scene.wait`` funnels its
        ``Wait`` animation through this method, so a second scaling there
        would stretch every hold twice — which is exactly the bug the first
        draft of this class had.
        """
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] /= PLAYBACK_SPEED
            return super().play(*animations, **kwargs)
        prepared = [prepare_animation(animation) for animation in animations]
        for animation in prepared:
            animation.run_time /= PLAYBACK_SPEED
        return super().play(*prepared, **kwargs)

    def title(self, label: str) -> VGroup:
        """Build the title block and remember it as ``self.head``.

        Returns the mobject rather than playing it, so the caller stays in
        control of how it enters::

            self.play(FadeIn(self.title("Combinations"), shift=0.3 * DOWN))
        """
        self.head = header(label)
        return self.head
