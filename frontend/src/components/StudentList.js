import React, { useState, useEffect } from 'react';
import axios from 'axios';

const StudentList = () => {
    const [students, setStudents] = useState([]);

    const fetchStudents = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/students');
            setStudents(response.data);
        } catch (error) {
            console.error('Error fetching students:', error);
        }
    };

    useEffect(() => {
        fetchStudents();
    }, []);

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/api/students/${id}`);
            fetchStudents();
        } catch (error) {
            console.error('Error deleting student:', error);
        }
    };

    return (
        <div>
            <h2>Students List</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Course</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {students.map((student) => (
                        <tr key={student.id}>
                            <td>{student.name}</td>
                            <td>{student.email}</td>
                            <td>{student.course}</td>
                            <td>
                                <button onClick={() => handleDelete(student.id)}>
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default StudentList;