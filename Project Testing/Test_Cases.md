# 📋 Project Test Cases - Rising Waters

| Test ID | Component | Description | Expected Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Authentication | Enter valid admin credentials (`admin` / `river2026`) | Successfully redirects user to `/home` dashboard | **PASSED** |
| **TC-02** | Authentication | Enter invalid credentials or blank spaces | Re-renders `login.html` with access denied error message | **PASSED** |
| **TC-03** | Model Loading | Initialize system execution via `py app.py` | Imports `floods.save` and `transform.save` without data crash | **PASSED** |
| **TC-04** | Form Validation | Submit alphanumeric characters into numeric form fields | Intercepts input safely and displays form parameter error | **PASSED** |
| **TC-05** | Core ML Pipeline | Submit extreme annual rainfall parameter (> 3000mm) | Triggers logic fallbacks and returns 🔴 HIGH ALERT status signal | **PASSED** |
