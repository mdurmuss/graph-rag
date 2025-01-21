// ------------------------------ NODES ------------------------------
// 1. create nodes for each Patient in the health data.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MERGE (p:Patient {name: row.Name})
SET p.age = toInteger(row.Age),
    p.gender = row.Gender,
    p.bloodType = row.Blood_Type;

// 2. create nodes for each medical condition in the health data.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MERGE (disease:Disease {name: row.`Medical Condition`});

// 3. create nodes for each doctor in the health data.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MERGE (d:Doctor {name: row.Doctor});

// 4. create nodes for each hospital in the health data.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MERGE (h:Hospital {name: row.Hospital});

// 5. create nodes for each insurance provider in the health data.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MERGE (i:InsuranceProvider {name: row.`Insurance Provider`});

// 6. create nodes for each medication in the health data.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MERGE (m:Medication {name: row.Medication});
// ------------------------------ EDGES ------------------------------
// 7. create relationships between people and their medical conditions.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MATCH (p:Patient {name: row.Name})
MATCH (disease:Disease {name: row.`Medical Condition`})
MERGE (p)-[:HAS_CONDITION]->(disease);

// 8. create relationships between people and their doctors.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MATCH (p:Patient {name: row.Name})
MATCH (d:Doctor {name: row.Doctor})
MERGE (p)-[:TREATED_BY]->(d);

// 9. create relationships between people and the hospitals they were admitted to.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MATCH (p:Patient {name: row.Name})
MATCH (h:Hospital {name: row.Hospital})
MERGE (p)-[r:ADMITTED_TO]->(h)
SET r.dateOfAdmission = row.`Date of Admission`,
    r.dischargeDate = row.`Discharge Date`,
    r.billingAmount = toFloat(row.`Billing Amount`),
    r.roomNumber = row.`Room Number`,
    r.admissionType = row.`Admission Type`,
    r.testResults = row.`Test Results`;

// 10. create relationships between people and their insurance providers.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MATCH (p:Patient {name: row.Name})
MATCH (i:InsuranceProvider {name: row.`Insurance Provider`})
MERGE (p)-[:INSURED_BY]->(i);

// 11. create relationships between people and the medications they take.
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MATCH (p:Patient {name: row.Name})
MATCH (m:Medication {name: row.Medication})
MERGE (p)-[:TAKES]->(m);