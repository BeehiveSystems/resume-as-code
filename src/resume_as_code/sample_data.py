from __future__ import annotations

from collections import OrderedDict


def build_sample_resume() -> OrderedDict:
    return OrderedDict(
        [
            ("version", 1),
            (
                "theme",
                OrderedDict(
                    [
                        ("name", "classic"),
                        ("accent_color", "#1f4f78"),
                    ]
                ),
            ),
            (
                "basics",
                OrderedDict(
                    [
                        ("name", "Jane Doe"),
                        ("role", "Staff Product Engineer"),
                        ("email", "jane@example.com"),
                        ("phone", "(555) 555-0100"),
                        ("location", "Brooklyn, NY"),
                        ("website", "https://janedoe.dev"),
                        (
                            "summary",
                            (
                                "Builder focused on developer tools, product systems, and the "
                                "operational details that make teams faster."
                            ),
                        ),
                        (
                            "profiles",
                            [
                                OrderedDict(
                                    [
                                        ("network", "LinkedIn"),
                                        ("username", "janedoe"),
                                        ("url", "https://linkedin.com/in/janedoe"),
                                    ]
                                ),
                                OrderedDict(
                                    [
                                        ("network", "GitHub"),
                                        ("username", "janedoe"),
                                        ("url", "https://github.com/janedoe"),
                                    ]
                                ),
                            ],
                        ),
                    ]
                ),
            ),
            (
                "skills",
                [
                    OrderedDict(
                        [
                            ("category", "Languages"),
                            ("items", ["Python", "TypeScript", "Go", "SQL"]),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("category", "Systems"),
                            ("items", ["Platform engineering", "APIs", "Developer experience"]),
                        ]
                    ),
                ],
            ),
            (
                "experience",
                [
                    OrderedDict(
                        [
                            ("company", "Acme Inc."),
                            ("title", "Staff Engineer"),
                            ("location", "Remote"),
                            ("start", "2022-01"),
                            ("end", "Present"),
                            (
                                "summary",
                                "Owned the internal developer platform used by six product teams.",
                            ),
                            (
                                "highlights",
                                [
                                    "Cut service onboarding time from two weeks to two days by standardizing templates and CI defaults.",
                                    "Designed an internal deployment control plane with strong guardrails and clear ownership boundaries.",
                                    "Partnered with recruiting and leadership to turn engineering impact into a clearer hiring narrative.",
                                ],
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("company", "Northstar Labs"),
                            ("title", "Senior Software Engineer"),
                            ("location", "New York, NY"),
                            ("start", "2019-06"),
                            ("end", "2021-12"),
                            (
                                "highlights",
                                [
                                    "Built customer-facing workflow tooling that reduced manual review time by 35 percent.",
                                    "Introduced shared design and telemetry patterns across a multi-product React and Python stack.",
                                ],
                            ),
                        ]
                    ),
                ],
            ),
            (
                "projects",
                [
                    OrderedDict(
                        [
                            ("name", "Release Graph"),
                            ("link", "https://example.com/release-graph"),
                            (
                                "description",
                                "Change intelligence dashboard for release readiness and incident correlation.",
                            ),
                            (
                                "highlights",
                                [
                                    "Used by engineering managers to review deployment risk before production pushes.",
                                ],
                            ),
                        ]
                    )
                ],
            ),
            (
                "education",
                [
                    OrderedDict(
                        [
                            ("institution", "Northeastern University"),
                            ("degree", "B.S. in Computer Science"),
                            ("location", "Boston, MA"),
                            ("start", "2014"),
                            ("end", "2018"),
                        ]
                    )
                ],
            ),
            (
                "certifications",
                [
                    OrderedDict(
                        [
                            ("name", "AWS Certified Solutions Architect"),
                            ("issuer", "Amazon Web Services"),
                            ("date", "2023"),
                        ]
                    )
                ],
            ),
        ]
    )

