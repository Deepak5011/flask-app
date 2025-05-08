// main.js for AJAX, modals, and form validation

document.addEventListener('DOMContentLoaded', function() {
    // Job Form Submission
    const jobForm = document.getElementById('jobForm');
    if (jobForm) {
        jobForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const id = document.getElementById('job_id').value;
            const data = {
                title: document.getElementById('job_title').value,
                category: document.getElementById('job_category').value,
                eligibility: document.getElementById('job_eligibility').value,
                description: document.getElementById('job_description').value,
                total_vacancy: document.getElementById('job_total_vacancy').value,
                exam_fee: document.getElementById('job_exam_fee').value,
                start_date_to_apply: document.getElementById('job_start_date').value,
                last_date_to_apply: document.getElementById('job_last_date').value,
                apply_link: document.getElementById('job_apply_link').value,
                pyq_link: document.getElementById('job_pyq_link').value
            };
            
            const url = id ? `/api/jobs/${id}` : '/api/jobs';
            const method = id ? 'PUT' : 'POST';
            
            fetch(url, {
                method: method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(err => {
                        throw new Error(err.error || 'Network response was not ok');
                    });
                }
                return res.json();
            })
            .then(res => {
                bootstrap.Modal.getOrCreateInstance(document.getElementById('jobModal')).hide();
                jobForm.reset();
                loadJobs();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving job: ' + error.message);
            });
        });
    }
    // Result Form Submission
    const resultForm = document.getElementById('resultForm');
    if (resultForm) {
        resultForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const id = document.getElementById('result_id').value;
            const data = {
                title: document.getElementById('result_title').value,
                link: document.getElementById('result_link').value,
                date_published: document.getElementById('result_date').value
            };
            
            const url = id ? `/api/results/${id}` : '/api/results';
            const method = id ? 'PUT' : 'POST';
            
            fetch(url, {
                method: method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(err => {
                        throw new Error(err.error || 'Network response was not ok');
                    });
                }
                return res.json();
            })
            .then(res => {
                bootstrap.Modal.getOrCreateInstance(document.getElementById('resultModal')).hide();
                resultForm.reset();
                loadResults();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving result: ' + error.message);
            });
        });
    }
    // Admit Card Form Submission
    const admitCardForm = document.getElementById('admitCardForm');
    if (admitCardForm) {
        admitCardForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const id = document.getElementById('admit_id').value;
            const data = {
                title: document.getElementById('admit_title').value,
                link: document.getElementById('admit_link').value,
                date_published: document.getElementById('admit_date').value
            };
            
            const url = id ? `/api/admit-cards/${id}` : '/api/admit-cards';
            const method = id ? 'PUT' : 'POST';
            
            fetch(url, {
                method: method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(err => {
                        throw new Error(err.error || 'Network response was not ok');
                    });
                }
                return res.json();
            })
            .then(res => {
                bootstrap.Modal.getOrCreateInstance(document.getElementById('admitCardModal')).hide();
                admitCardForm.reset();
                loadAdmitCards();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving admit card: ' + error.message);
            });
        });
    }
    // Load Jobs
    window.loadJobs = function() {
        fetch('/api/jobs')
            .then(res => res.json())
            .then(jobs => {
                let html = '<table class="table table-bordered"><thead><tr><th>Title</th><th>Category</th><th>Eligibility</th><th>Actions</th></tr></thead><tbody>';
                jobs.forEach(job => {
                    html += `<tr>
                        <td>${job.title}</td>
                        <td>${job.category || ''}</td>
                        <td>${job.eligibility || ''}</td>
                        <td>
                            <button class='btn btn-sm btn-primary' onclick='editJob(${JSON.stringify(job)})'>Edit</button>
                            <button class='btn btn-sm btn-danger' onclick='deleteJob("${job._id}")'>Delete</button>
                        </td>
                    </tr>`;
                });
                html += '</tbody></table>';
                document.getElementById('admin-jobs-list').innerHTML = html;
            });
    }
    
    // Edit Job
    window.editJob = function(job) {
        document.getElementById('job_id').value = job._id;
        document.getElementById('job_title').value = job.title;
        document.getElementById('job_category').value = job.category || '';
        document.getElementById('job_eligibility').value = job.eligibility || '';
        document.getElementById('job_description').value = job.description || '';
        document.getElementById('job_total_vacancy').value = job.total_vacancy || '';
        document.getElementById('job_exam_fee').value = job.exam_fee || '';
        document.getElementById('job_start_date').value = job.start_date_to_apply || '';
        document.getElementById('job_last_date').value = job.last_date_to_apply || '';
        document.getElementById('job_apply_link').value = job.apply_link || '';
        document.getElementById('job_pyq_link').value = job.pyq_link || '';
        bootstrap.Modal.getOrCreateInstance(document.getElementById('jobModal')).show();
    }
    
    // Delete Job
    window.deleteJob = function(id) {
        if(confirm('Are you sure you want to delete this job?')) {
            fetch(`/api/jobs/${id}`, {method:'DELETE'})
                .then(() => loadJobs());
        }
    }
    // Load Results
    window.loadResults = function() {
        fetch('/api/results')
            .then(res => res.json())
            .then(results => {
                let html = '<table class="table table-bordered"><thead><tr><th>Title</th><th>Link</th><th>Date</th><th>Actions</th></tr></thead><tbody>';
                results.forEach(result => {
                    html += `<tr>
                        <td>${result.title}</td>
                        <td><a href='${result.link}' target='_blank'>View</a></td>
                        <td>${result.date_published || ''}</td>
                        <td>
                            <button class='btn btn-sm btn-primary' onclick='editResult(${JSON.stringify(result)})'>Edit</button>
                            <button class='btn btn-sm btn-danger' onclick='deleteResult("${result._id}")'>Delete</button>
                        </td>
                    </tr>`;
                });
                html += '</tbody></table>';
                document.getElementById('admin-results-list').innerHTML = html;
            });
    }
    
    // Edit Result
    window.editResult = function(result) {
        document.getElementById('result_id').value = result._id;
        document.getElementById('result_title').value = result.title;
        document.getElementById('result_link').value = result.link || '';
        document.getElementById('result_date').value = result.date_published || '';
        bootstrap.Modal.getOrCreateInstance(document.getElementById('resultModal')).show();
    }
    
    // Delete Result
    window.deleteResult = function(id) {
        if(confirm('Are you sure you want to delete this result?')) {
            fetch(`/api/results/${id}`, {method:'DELETE'})
                .then(() => loadResults());
        }
    }
    // Load Admit Cards
    window.loadAdmitCards = function() {
        fetch('/api/admit-cards')
            .then(res => res.json())
            .then(admitCards => {
                let html = '<table class="table table-bordered"><thead><tr><th>Title</th><th>Link</th><th>Date</th><th>Actions</th></tr></thead><tbody>';
                admitCards.forEach(admit => {
                    html += `<tr>
                        <td>${admit.title}</td>
                        <td><a href='${admit.link}' target='_blank'>View</a></td>
                        <td>${admit.date_published || ''}</td>
                        <td>
                            <button class='btn btn-sm btn-primary' onclick='editAdmitCard(${JSON.stringify(admit)})'>Edit</button>
                            <button class='btn btn-sm btn-danger' onclick='deleteAdmitCard("${admit._id}")'>Delete</button>
                        </td>
                    </tr>`;
                });
                html += '</tbody></table>';
                document.getElementById('admin-admit-cards-list').innerHTML = html;
            });
    }
    
    // Edit Admit Card
    window.editAdmitCard = function(admit) {
        document.getElementById('admit_id').value = admit._id;
        document.getElementById('admit_title').value = admit.title;
        document.getElementById('admit_link').value = admit.link || '';
        document.getElementById('admit_date').value = admit.date_published || '';
        bootstrap.Modal.getOrCreateInstance(document.getElementById('admitCardModal')).show();
    }
    
    // Delete Admit Card
    window.deleteAdmitCard = function(id) {
        if(confirm('Are you sure you want to delete this admit card?')) {
            fetch(`/api/admit-cards/${id}`, {method:'DELETE'})
                .then(() => loadAdmitCards());
        }
    }
    // Initial load
    if (document.getElementById('admin-jobs-list')) loadJobs();
    if (document.getElementById('admin-results-list')) loadResults();
    if (document.getElementById('admin-admit-cards-list')) loadAdmitCards();
});

// Modal open functions for compatibility
function openJobModal() { 
    document.getElementById('jobForm').reset(); 
    document.getElementById('job_id').value = '';
    bootstrap.Modal.getOrCreateInstance(document.getElementById('jobModal')).show();
}

function openResultModal() { 
    document.getElementById('resultForm').reset(); 
    document.getElementById('result_id').value = '';
    bootstrap.Modal.getOrCreateInstance(document.getElementById('resultModal')).show();
}

function openAdmitCardModal() { 
    document.getElementById('admitCardForm').reset(); 
    document.getElementById('admit_id').value = '';
    bootstrap.Modal.getOrCreateInstance(document.getElementById('admitCardModal')).show();
}