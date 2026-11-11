from abc import ABC, abstractmethod

class ScreeningProcess(ABC):
    @abstractmethod
    def screen(self, candidate, job):
        pass

class Candidate:
    def __init__(self, name, skills, experience, qualification):
        self.__name = name
        self.__skills = skills
        self.__experience = experience
        self.__qualification = qualification

    def get_name(self): return self.__name
    def get_skills(self): return self.__skills
    def get_experience(self): return self.__experience
    def get_qualification(self): return self.__qualification

    def calculate_match(self, job):
        matched = 0
        missing = []
        for s in job.get_required_skills():
            if s.lower() in [x.lower() for x in self.__skills]:
                matched += 1
            else:
                missing.append(s)
        percent = (matched / len(job.get_required_skills())) * 100
        return percent, missing

class FresherCandidate(Candidate):
    def __init__(self, name, skills, qualification):
        super().__init__(name, skills, 0, qualification)
    def is_eligible(self, job):
        return True

class ExperiencedCandidate(Candidate):
    def __init__(self, name, skills, experience, qualification):
        super().__init__(name, skills, experience, qualification)
    def is_eligible(self, job):
        return self.get_experience() >= job.get_min_experience()

class Job:
    def __init__(self, title, required_skills, min_experience):
        self.__title = title
        self.__required_skills = required_skills
        self.__min_experience = min_experience
    def get_title(self): return self.__title
    def get_required_skills(self): return self.__required_skills
    def get_min_experience(self): return self.__min_experience

class ResumeScreening(ScreeningProcess):
    def screen(self, candidate, job):
        percent, missing = candidate.calculate_match(job)
        exp_ok = candidate.is_eligible(job)
        if percent >= 50 and exp_ok:
            status = "SHORTLISTED"
            reason = "All requirements met."
        else:
            status = "REJECTED"
            reason = f"Skill match only {percent:.0f}% (Need 50%+) | Missing: {', '.join(missing)}"
        return percent, exp_ok, status, reason, missing

job = Job("Python Developer", ["Python", "SQL", "HTML"], 1)

candidates = [
    FresherCandidate("Vishwa", ["Python", "SQL", "HTML"], "BCA"),
    ExperiencedCandidate("Jayashree", ["Python", "Java"], 2, "EEE"),
    ExperiencedCandidate("Anto", ["Python", "SQL", "HTML", "Django"], 3, "IT"),
    FresherCandidate("Vinoth", ["Java", "HTML"], "CSE")
]

screener = ResumeScreening()

# Top Header
print("\n  ★ ═══════════════════════════════ ★")
print("       RESUME SCREENING SYSTEM")
print("  ★ ═══════════════════════════════ ★")
print("  Job : Python Developer | Required : Python, SQL, HTML")
print("  Total Candidates : 4")

shortlisted = 0

for i, c in enumerate(candidates, 1):
    percent, exp_ok, status, reason, missing = screener.screen(c, job)
    if status == "SHORTLISTED":
        shortlisted += 1

    # ONE PERSON = ONE BLOCK ONLY
    print("\n  ✦ ─────────────────────────────── ✦")
    print(f"  CANDIDATE {i} : {c.get_name()}")
    print(f"  Qualification : {c.get_qualification()}")
    print(f"  Skills        : {', '.join(c.get_skills())}")
    print(f"  Experience    : {c.get_experience()} yrs")
    print(f"  Skill Match   : {percent:.0f}%  |  Exp Eligible : {'Yes' if exp_ok else 'No'}")
    print(f"  STATUS        : {status}")
    print(f"  Reason        : {reason}")
    if status == "REJECTED":
        print(f"  Tip           : Learn {', '.join(missing)}")
    print("  ✦ ─────────────────────────────── ✦")

# Summary - One Block
print("\n  ★ ═══════════════════════════════ ★")
print("       FINAL SUMMARY")
print(f"  Shortlisted : {shortlisted} | Rejected : {len(candidates) - shortlisted}")
print(f"  Topper : Rahul, Arjun")
print("  ★ ═══════════════════════════════ ★")
print("       Thank You !")