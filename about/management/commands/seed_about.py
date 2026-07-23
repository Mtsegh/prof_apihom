"""
Seed data — about app
======================
Source: prof. IhomCURRICULUM VITAE.doc 2023.docx
Models seeded: AboutContent, Education, CareerMilestone, Membership, Skill
(about/models.py)

Place this file at:
    about/management/commands/seed_about.py

(about/management/__init__.py and about/management/commands/__init__.py
must also exist — both included alongside this file.)

Run with:
    python manage.py seed_about
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from about.models import AboutContent, CareerMilestone, Education, Membership, Skill


class Command(BaseCommand):
    help = (
        "Seed the about app: AboutContent, Education, CareerMilestone, "
        "Membership, and Skill records for Prof. A.P. Ihom."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        self.seed_about_content()
        self.seed_education()
        self.seed_career_milestones()
        self.seed_memberships()
        self.seed_skills()
        self.stdout.write(self.style.SUCCESS("about: seeding complete."))

    def seed_about_content(self):
        content = AboutContent.load()

        content.full_bio = (
            "Professor Aondona Paul Ihom is a researcher and academician "
            "in Materials, Production and Industrial Engineering at the "
            "University of Uyo, where he has supervised and examined "
            "postgraduate students both locally and internationally. His "
            "research and teaching draw on more than two decades of "
            "industrial experience that shaped his approach to research "
            "and innovation in engineering.\n\n"

            "He earned his B.Eng. in Materials and Metallurgical "
            "Engineering from the University of Jos in 1991, followed by "
            "an M.Eng. in Mechanical Engineering from the University of "
            "Agriculture, Makurdi, and a PhD in Materials and "
            "Metallurgical Engineering from Abubakar Tafawa Balewa "
            "University, Bauchi, in 2009. He also holds a Postgraduate "
            "Diploma and an MBA in Management from Imo State University, "
            "Owerri.\n\n"

            "His career began in 1991 with the National Youth Service "
            "Corps at Adiabong Girls Secondary School in Nsit Ubium, Akwa "
            "Ibom State, followed by a period as a Graduate Assistant at "
            "Mkar University. In 1997 he joined the National "
            "Metallurgical Development Centre in Jos, where he spent "
            "fifteen years rising to the rank of Chief Metallurgical "
            "Engineer and serving as Head of the Foundry and Heat "
            "Treatment Section — a period that included an industrial "
            "training placement in Japan focused on durable materials "
            "and machine production. During this time, he contributed to "
            "the design and production of agricultural and industrial "
            "machinery, including a melon peeling machine and work in 3D "
            "printing and additive manufacturing.\n\n"

            "He joined the University of Uyo in 2012 as a Senior "
            "Lecturer in the Mechanical Engineering Department, was "
            "promoted to Associate Professor in 2015, and became a full "
            "Professor in 2018. Beyond teaching and research, he has "
            "held academic leadership roles including Departmental "
            "Postgraduate Coordinator, Faculty of Engineering "
            "Postgraduate Coordinator, Acting Head of the Mechanical and "
            "Aerospace Engineering Department, Vice Dean, and Acting "
            "Dean of the Faculty of Engineering.\n\n"

            "His research spans materials and metallurgical engineering, "
            "production and industrial engineering, and energy and "
            "environmental protection, with a publication record of over "
            "200 works spanning journal articles, books, and "
            "peer-reviewed conference proceedings. He serves as an "
            "editor and reviewer for journals in several countries and "
            "was Managing Editor of the Journal of Research and "
            "Innovations in Engineering (JORIE) at the University of Uyo "
            "for four years.\n\n"

            "He is a COREN-registered engineer and a member of several "
            "professional bodies, having served the Nigerian Society of "
            "Engineers' Jos branch as PRO, Assistant Secretary, and "
            "Secretary, and the Nigerian Metallurgical Society as "
            "Secretary and later National Vice President. He was elected "
            "a Fellow of the Nigerian Metallurgical Society in 2011 and "
            "a Fellow of the Institute of Policy Management and "
            "Leadership Development in 2026.\n\n"

            "Outside the university, he has been an active community "
            "leader in his home village of Hwollaza in Bassa Local "
            "Government Area, Plateau State, serving for many years as "
            "community development chairman. He is a committed Christian "
            "who has served as a Deacon, church treasurer, and men's "
            "president at the Assemblies of God Church in Hwollaza, Jos. "
            "He is happily married with six children, and his interests "
            "include reading, research, and Christian music."
        )

        content.academic_journey = (
            "Professor Ihom's academic path began with a B.Eng. in "
            "Materials and Metallurgical Engineering from the University "
            "of Jos (1991), followed by an M.Eng. in Mechanical "
            "Engineering from the University of Agriculture, Makurdi, "
            "and a PhD in Materials and Metallurgical Engineering from "
            "Abubakar Tafawa Balewa University, Bauchi (2009). Alongside "
            "his engineering training, he completed a Postgraduate "
            "Diploma and an MBA in Management from Imo State University, "
            "Owerri, rounding out a career built on both technical depth "
            "and administrative capability."
        )

        # TODO: no explicit teaching-philosophy statement appears anywhere
        # in the CV — left blank until Prof. Ihom supplies one.
        content.teaching_philosophy = ""

        content.save()

    def seed_education(self):
        # end_year uses the CONFERRAL year throughout, per instruction —
        # this resolves several attendance-range vs. conferral-year
        # mismatches in the source (see notes on individual records).
        #
        # Two CV-listed certificates are intentionally NOT included below,
        # because the source gives no institution or location for either
        # one, and Education.institution is a required field:
        #   - Certificate in Japanese Language (2008)
        #   - Certificate in Metallography and Microscopy Evaluation of
        #     Metallic, Non-metallic Materials and their Alloys (2012)
        # Supply an institution for either and they can be added.
        records = [
            dict(
                institution="Government College Katsina-Ala",
                degree="O' Level GCE",
                start_year=1981,
                end_year=1986,
                order=0,
            ),
            dict(
                institution="University of Jos",
                degree="B.Eng., Materials and Metallurgical Engineering",
                start_year=1986,
                end_year=1991,
                order=1,
            ),
            dict(
                institution="University of Agriculture, Makurdi",
                degree="M.Eng., Mechanical Engineering",
                # NOTE: the CV's "institutions attended" list gives
                # 1995-1998 for this university; the "academic
                # qualifications" list gives 2001 as the conferral year.
                # start_year keeps the explicit attendance-start date;
                # end_year uses the conferral year.
                start_year=1995,
                end_year=2001,
                order=2,
            ),
            dict(
                institution="Imo State University, Owerri",
                degree="Postgraduate Diploma in Management (PGDM)",
                start_year=1999,
                end_year=2001,
                order=3,
            ),
            dict(
                institution="Imo State University, Owerri",
                degree="MBA, Management",
                # NOTE: the CV's attendance range for Imo State
                # (1999-2003) doesn't reach this degree's own conferral
                # year (2005), so start_year is left unset rather than
                # reused from the PGDM record above.
                start_year=None,
                end_year=2005,
                order=4,
            ),
            dict(
                institution="Abubakar Tafawa Balewa University, Bauchi",
                degree="PhD, Materials and Metallurgical Engineering",
                # NOTE: the CV's "institutions attended" list gives
                # 2004-2008; both the bio narrative and the academic
                # qualifications list give 2009 as the year the PhD was
                # conferred.
                start_year=2004,
                end_year=2009,
                order=5,
            ),
            dict(
                # The CV names this certificate's location only as
                # "(Japan)" — no specific school or training body given.
                institution="Japan",
                degree=(
                    "Certificate in Heat Treatment, Corrosion, and "
                    "Surface Finishing Technology for Improving Metal "
                    "Property"
                ),
                start_year=None,
                end_year=2008,
                order=6,
            ),
        ]
        for rec in records:
            Education.objects.update_or_create(
                institution=rec["institution"],
                degree=rec["degree"],
                defaults={
                    "start_year": rec["start_year"],
                    "end_year": rec["end_year"],
                    "order": rec["order"],
                },
            )

    def seed_career_milestones(self):
        # The CV's own "2015-2018 Associate Professor, Mechanical and
        # Aerospace Engineering Department, University of Uyo" line
        # appears twice, verbatim back-to-back — collapsed to one record
        # here.
        #
        # "Ag HOD, Mechanical and Aerospace Engineering" is also listed
        # among Prof. Ihom's administrative responsibilities, but no year
        # is given anywhere in the CV for this role, and start_year is
        # required — so it's omitted rather than guessed. Supply a year
        # and it can be added.
        records = [
            dict(
                title="Tutor (NYSC)",
                organization=(
                    "Adiabong Girls Secondary School, Ikot Imoh, Nsit "
                    "Ubium LGA, Akwa Ibom State"
                ),
                start_year=1991,
                end_year=1992,
                description="Taught mathematics, physics, and chemistry.",
            ),
            dict(
                title="Graduate Assistant",
                organization=(
                    "Institute for Christian Studies, Mkar University, "
                    "Benue State"
                ),
                start_year=1993,
                end_year=1995,
                description=(
                    "Prepared pre-degree students and taught technical "
                    "education courses, including engineering drawing "
                    "and foundry technology."
                ),
            ),
            dict(
                # Concurrent with the Part-time Lecturer role below —
                # modeled as two separate records since they're two
                # distinct organizations, not one row's description.
                title="Manager",
                organization="Abdos Tractor Hiring Company",
                start_year=1995,
                end_year=1996,
                description="In charge of tractor maintenance and routing.",
            ),
            dict(
                title="Part-time Lecturer",
                organization=(
                    "Benue Institute for Management and Technology, "
                    "Mkar, Gboko"
                ),
                start_year=1995,
                end_year=1996,
                description="Taught foundry technology.",
            ),
            dict(
                title="Metallurgical Engineer I",
                organization="National Metallurgical Development Centre, Jos",
                start_year=1997,
                end_year=2001,
                description=(
                    "Research on heat treatment and foundry raw "
                    "materials, and development of casting techniques, "
                    "ceramics, refractories, and glass products."
                ),
            ),
            dict(
                title="Senior Metallurgical Engineer",
                organization="National Metallurgical Development Centre, Jos",
                start_year=2001,
                end_year=2004,
                description=(
                    "Continued research responsibilities, plus handling "
                    "outside jobs from higher institutions, individuals, "
                    "and corporate bodies."
                ),
            ),
            dict(
                title="Principal Metallurgical Engineer",
                organization="National Metallurgical Development Centre, Jos",
                start_year=2004,
                end_year=2007,
                description=(
                    "Continued research responsibilities, plus training "
                    "attachees on industrial training."
                ),
            ),
            dict(
                title="Assistant Chief Metallurgical Engineer",
                organization="National Metallurgical Development Centre, Jos",
                start_year=2007,
                end_year=2010,
                description=(
                    "Continued research responsibilities, with "
                    "additional administrative responsibility as head "
                    "of the unit."
                ),
            ),
            dict(
                title=(
                    "Chief Metallurgical Engineer / Head of Heat "
                    "Treatment and Foundry Section"
                ),
                organization="National Metallurgical Development Centre, Jos",
                start_year=2010,
                end_year=2012,
                description=(
                    "Responsible for the day-to-day running of the Heat "
                    "Treatment and Foundry Section, and other duties "
                    "assigned by the Head of Department and the "
                    "Director General."
                ),
            ),
            dict(
                title="Senior Lecturer",
                organization=(
                    "Mechanical Engineering Department, University of Uyo"
                ),
                start_year=2012,
                end_year=2015,
                description=(
                    "Teaching, examination supervision, and project "
                    "supervision at undergraduate and postgraduate "
                    "levels, alongside research and departmental/"
                    "faculty duties."
                ),
            ),
            dict(
                title="Associate Professor",
                organization=(
                    "Mechanical and Aerospace Engineering Department, "
                    "University of Uyo"
                ),
                start_year=2015,
                end_year=2018,
                description=(
                    "Teaching, examination supervision, and project "
                    "supervision at undergraduate and postgraduate "
                    "levels, alongside research and departmental/"
                    "faculty duties."
                ),
            ),
            dict(
                title="Professor",
                organization=(
                    "Mechanical and Aerospace Engineering Department, "
                    "University of Uyo"
                ),
                start_year=2018,
                end_year=None,  # current position
                description=(
                    "Teaching, examination supervision, and project "
                    "supervision at undergraduate and postgraduate "
                    "levels, alongside research and departmental/"
                    "faculty duties."
                ),
            ),
            dict(
                title="Senate Member",
                organization="University of Uyo Senate",
                start_year=2016,
                end_year=2017,
                description="",
            ),
            dict(
                title="Vice Dean",
                organization="Faculty of Engineering, University of Uyo",
                start_year=2016,
                end_year=2020,
                description="",
            ),
            dict(
                title="Acting Dean",
                organization="Faculty of Engineering, University of Uyo",
                start_year=2017,
                end_year=2017,
                description="August–November 2017.",
            ),
        ]
        for rec in records:
            CareerMilestone.objects.update_or_create(
                title=rec["title"],
                organization=rec["organization"],
                start_year=rec["start_year"],
                defaults={
                    "end_year": rec["end_year"],
                    "description": rec["description"],
                },
            )

    def seed_memberships(self):
        # Registration/membership numbers are folded into `role` rather
        # than `organization`, so organization names stay clean for
        # display.
        records = [
            dict(
                organization="Foundry Association of Nigeria",
                role="Member",
                year_joined=1997,
            ),
            dict(
                organization="Nigerian Metallurgical Society",
                role="Member (Reg. C484)",
                year_joined=1998,
            ),
            dict(
                organization="Nigerian Society of Engineers",
                role="Member (Reg. 12,158)",
                year_joined=2002,
            ),
            dict(
                organization="Nigerian Corrosion Association",
                role="Member (Reg. NICA 2003/010)",
                year_joined=2003,
            ),
            dict(
                organization=(
                    "Council for the Regulation of Engineering in "
                    "Nigeria (COREN)"
                ),
                role="Registered Engineer (R.10,557)",
                year_joined=2004,
            ),
            dict(
                organization="Corrosion Institute of South Africa",
                role="Member (Reg. IHO001)",
                year_joined=2015,
            ),
            dict(
                organization=(
                    "Materials Science and Technology Society of Nigeria"
                ),
                role="Member (Reg. P/1305)",
                year_joined=2015,
            ),
            dict(
                organization="Nigerian Institution of Mechanical Engineers",
                role="Member",
                year_joined=2016,
            ),
        ]
        for rec in records:
            Membership.objects.update_or_create(
                organization=rec["organization"],
                defaults={
                    "role": rec["role"],
                    "year_joined": rec["year_joined"],
                },
            )

    def seed_skills(self):
        # NOTE: the CV has no dedicated "Skills" section. This list is
        # compiled from skills evidenced indirectly throughout the CV —
        # courses taught, tools/methods named in publications, and
        # completed certificates — grouped by category, per instruction.
        # Treat this as a first draft; edit freely.
        records = [
            dict(name="Foundry Technology", category="Technical"),
            dict(
                name="Heat Treatment & Surface Engineering",
                category="Technical",
            ),
            dict(name="Corrosion Science", category="Technical"),
            dict(name="Materials Characterization", category="Technical"),
            dict(
                name="Nanomaterials & Composites Development",
                category="Technical",
            ),
            dict(
                name="Quality Control & Reliability Management",
                category="Technical",
            ),
            dict(name="MATLAB", category="Software & Analytical Tools"),
            dict(
                name="Statistical & Regression Modeling",
                category="Software & Analytical Tools",
            ),
            dict(
                name="Advanced Statistical Experimental Design",
                category="Software & Analytical Tools",
            ),
            dict(name="Japanese", category="Languages"),
        ]
        for rec in records:
            Skill.objects.update_or_create(
                name=rec["name"],
                defaults={"category": rec["category"]},
            )
