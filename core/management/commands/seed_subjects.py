from django.core.management.base import BaseCommand
from core.models import Branch, Semester, Subject


class Command(BaseCommand):
    help = "Seed branches, semesters, and subjects (Branch-wise + Semester-wise)"

    def handle(self, *args, **options):
        # ---------- BRANCHES ----------
        branch_names = [
            "Electronics and communication Engineering",
            "Computer science Engineering",
            "computer science (AI&ML)",
            "Civil Engineering",
            "Mechanical Engineering",
        ]

        branches = {}
        for b in branch_names:
            obj, created = Branch.objects.get_or_create(name=b)
            branches[b] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Branch: {b}"))
            else:
                self.stdout.write(self.style.WARNING(f"Branch exists: {b}"))

        # ---------- SEMESTERS ----------
        semesters = {}
        for i in range(1, 9):
            sem_obj, created = Semester.objects.get_or_create(number=i)
            semesters[i] = sem_obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Semester: {i}"))
            else:
                self.stdout.write(self.style.WARNING(f"Semester exists: {i}"))

        # ---------- SUBJECTS DATA ----------
        subjects_data = {
            "Electronics and communication Engineering": {
                1: [
                    "Matrices and Calculus",
                    "Applied Physics",
                    "Engineering Chemistry",
                    "C Programming and Data Structures",
                    "English for Skill Enhancement",
                ],
                2: [
                    "Ordinary Differential Equations and Vector Calculus",
                    "Engineering Chemistry",
                    "Engineering Mechanics",
                    "Python Programming",
                    "Engineering Graphics",
                ],
                3: [
                    "Network Theory",
                    "Signals and Systems",
                    "Electronic Devices and Circuits",
                    "Digital System Design",
                    "Probability and Random Processes",
                ],
                4: [
                    "Analog Circuits",
                    "Control Systems",
                    "Analog Communications",
                    "Microprocessors and Microcontrollers",
                    "Electromagnetic Fields",
                ],
                5: [
                    "Digital Communications",
                    "VLSI Design",
                    "Antennas and Wave Propagation",
                    "Embedded Systems",
                    "Linear IC Applications",
                ],
                6: [
                    "Wireless Communication",
                    "IoT",
                    "Digital Signal Processing",
                    "Microwave Engineering",
                    "Optical Communication",
                ],
                7: [
                    "Mobile Communication",
                    "Cyber Security Basics",
                    "Machine Learning Basics",
                    "Open Elective - I",
                    "Professional Elective - I",
                ],
                8: [
                    "Project Work",
                    "Internship / Industrial Training",
                    "Seminar",
                ],
            },

            "Computer science Engineering": {
                1: [
                    "Matrices and Calculus",
                    "Applied Physics",
                    "Engineering Chemistry",
                    "C Programming and Data Structures",
                    "English for Skill Enhancement",
                ],
                2: [
                    "Ordinary Differential Equations and Vector Calculus",
                    "Engineering Chemistry",
                    "Engineering Mechanics",
                    "Python Programming",
                    "Engineering Graphics",
                ],
                3: [
                    "Discrete Mathematics",
                    "Data Structures",
                    "Digital Logic Design",
                    "Computer Organization",
                    "OOP with Java",
                ],
                4: [
                    "DBMS",
                    "Operating Systems",
                    "Design and Analysis of Algorithms",
                    "Software Engineering",
                    "Probability and Statistics",
                ],
                5: [
                    "Computer Networks",
                    "Web Technologies",
                    "Compiler Design",
                    "Artificial Intelligence",
                    "Machine Learning",
                ],
                6: [
                    "Cloud Computing",
                    "Data Science",
                    "Cyber Security",
                    "Distributed Systems",
                    "Open Elective - I",
                ],
                7: [
                    "Big Data Analytics",
                    "DevOps",
                    "Blockchain Basics",
                    "Professional Elective - I",
                    "Professional Elective - II",
                ],
                8: [
                    "Project Work",
                    "Internship / Industrial Training",
                    "Seminar",
                ],
            },

            "computer science (AI&ML)": {
                1: [
                    "Matrices and Calculus",
                    "Applied Physics",
                    "Engineering Chemistry",
                    "C Programming and Data Structures",
                    "English for Skill Enhancement",
                ],
                2: [
                    "Ordinary Differential Equations and Vector Calculus",
                    "Engineering Chemistry",
                    "Engineering Mechanics",
                    "Python Programming",
                    "Engineering Graphics",
                ],
                3: [
                    "Discrete Mathematics",
                    "Data Structures",
                    "Digital Logic Design",
                    "Computer Organization",
                    "OOP with Java",
                ],
                4: [
                    "DBMS",
                    "Operating Systems",
                    "Design and Analysis of Algorithms",
                    "Probability and Statistics",
                    "Foundations of AI",
                ],
                5: [
                    "Machine Learning",
                    "Deep Learning",
                    "Computer Vision",
                    "Natural Language Processing",
                    "Data Mining",
                ],
                6: [
                    "Reinforcement Learning",
                    "Cloud Computing",
                    "Big Data Analytics",
                    "AI Ethics",
                    "Open Elective - I",
                ],
                7: [
                    "MLOps",
                    "Advanced NLP",
                    "Advanced Computer Vision",
                    "Professional Elective - I",
                    "Professional Elective - II",
                ],
                8: [
                    "Project Work",
                    "Internship / Industrial Training",
                    "Seminar",
                ],
            },

            "Civil Engineering": {
                1: [
                    "Matrices and Calculus",
                    "Applied Physics",
                    "Engineering Chemistry",
                    "C Programming and Data Structures",
                    "English for Skill Enhancement",
                ],
                2: [
                    "Ordinary Differential Equations and Vector Calculus",
                    "Engineering Chemistry",
                    "Engineering Mechanics",
                    "Python Programming",
                    "Engineering Graphics",
                ],
                3: [
                    "Surveying",
                    "Strength of Materials",
                    "Building Materials",
                    "Fluid Mechanics",
                    "Engineering Geology",
                ],
                4: [
                    "Concrete Technology",
                    "Structural Analysis",
                    "Geotechnical Engineering",
                    "Hydraulics and Hydraulic Machines",
                    "Environmental Engineering",
                ],
                5: [
                    "Design of RCC Structures",
                    "Transportation Engineering",
                    "Water Resources Engineering",
                    "Steel Structures",
                    "Open Elective - I",
                ],
                6: [
                    "Foundation Engineering",
                    "Construction Management",
                    "Estimating and Costing",
                    "Remote Sensing and GIS",
                    "Professional Elective - I",
                ],
                7: [
                    "Advanced Structural Design",
                    "Smart Materials",
                    "Green Buildings",
                    "Professional Elective - II",
                    "Professional Elective - III",
                ],
                8: [
                    "Project Work",
                    "Internship / Industrial Training",
                    "Seminar",
                ],
            },

            "Mechanical Engineering": {
                1: [
                    "Matrices and Calculus",
                    "Applied Physics",
                    "Engineering Chemistry",
                    "C Programming and Data Structures",
                    "English for Skill Enhancement",
                ],
                2: [
                    "Ordinary Differential Equations and Vector Calculus",
                    "Engineering Chemistry",
                    "Engineering Mechanics",
                    "Python Programming",
                    "Engineering Graphics",
                ],
                3: [
                    "Mechanics of Solids",
                    "Thermodynamics",
                    "Metallurgy and Material Science",
                    "Production Technology",
                    "Engineering Drawing",
                ],
                4: [
                    "Kinematics of Machinery",
                    "Fluid Mechanics and Hydraulic Machines",
                    "IC Engines and Gas Turbines",
                    "Instrumentation and Control Systems",
                    "Basic Electrical and Electronics Engineering",
                ],
                5: [
                    "Dynamics of Machinery",
                    "Heat Transfer",
                    "Machine Design",
                    "Manufacturing Processes",
                    "Open Elective - I",
                ],
                6: [
                    "CAD/CAM",
                    "Finite Element Methods",
                    "Refrigeration and Air Conditioning",
                    "Industrial Engineering",
                    "Professional Elective - I",
                ],
                7: [
                    "Robotics",
                    "Automobile Engineering",
                    "Renewable Energy Systems",
                    "Professional Elective - II",
                    "Professional Elective - III",
                ],
                8: [
                    "Project Work",
                    "Internship / Industrial Training",
                    "Seminar",
                ],
            },
        }

        # ---------- INSERT SUBJECTS ----------
        total_created = 0

        for branch_name, sem_map in subjects_data.items():
            branch_obj = branches[branch_name]

            for sem_number, subject_list in sem_map.items():
                sem_obj = semesters[sem_number]

                for sub_name in subject_list:
                    sub_obj, created = Subject.objects.get_or_create(
                        branch=branch_obj,
                        semester=sem_obj,
                        name=sub_name
                    )
                    if created:
                        total_created += 1

        self.stdout.write(self.style.SUCCESS(f"\n✅ Done! Total new subjects added: {total_created}\n"))
