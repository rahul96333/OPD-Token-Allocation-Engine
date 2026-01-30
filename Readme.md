OPD Token Allocation Engine
Project Overview
This system is a backend API service designed to manage hospital doctor schedules and patient queues. It handles fixed time slots, enforces capacity limits, and dynamically prioritizes patients based on the urgency of their visit.

Prioritization Logic 

The system uses a weighted priority scale (1 to 5). A lower number indicates a higher medical priority:

Emergency (Priority 1): Highest priority. These patients can displace lower-priority patients even if a slot is full.


Paid Priority (Priority 2): High priority for premium booking.


Follow-up (Priority 3): Standard priority for returning patients.


Online Booking (Priority 4): Standard digital booking.


Walk-in (Priority 5): Standard physical booking.

Algorithm Design 

The core allocation algorithm follows these rules:

Hard Limit Enforcement: Each slot has a max_capacity. No regular patient can exceed this limit.


Dynamic Reallocation: If an Emergency patient arrives and the slot is full, the algorithm identifies the patient with the lowest priority currently in the slot.


The Swap: The low-priority patient is moved to an overflow (waiting) list, and the Emergency patient is inserted into the active slot.


Overflow Management: Patients who cannot fit into the current slot are held in a secondary queue to be processed if a cancellation occurs.

Edge Cases Handled 

Full Slot Emergencies: Handled by displacing the lowest-priority "Walk-in" or "Online" patient.


Duplicate Doctors: The system supports a minimum of 3 doctors simultaneously (Dr. Sharma, Dr. Reddy, Dr. Kapoor).

Invalid Sources: Any unknown booking source is automatically treated as a low-priority "Walk-in."

Failure Handling 

Input Validation: The API checks for missing doctor names or invalid patient types to prevent crashes.

In-Memory Continuity: For this simulation, data is stored in memory. For a production environment, a database like PostgreSQL would be used to prevent data loss during a server restart.

How to Run the Simulation 

Start Server: Run py -m uvicorn main:app --reload in your terminal.

Run Simulation: In a second terminal, run py simulation.py.

View Results: Open http://127.0.0.1:8000/view-status to see the final day's report across all 3 doctors.

What to submit now?
You now have all the deliverables requested in the PDF:


main.py: API Design & Allocation Algorithm.


simulation.py: One-day simulation with 3 doctors.



README.md: Documentation on logic, edge cases, and failures.

.......................................................................... YOU CAN VIEW THE WEB-PAGE ON http://127.0.0.1:8000/docs ..................................................................................
