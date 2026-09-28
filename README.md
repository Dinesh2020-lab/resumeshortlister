# Resume Shortlisting System

A rule-based Resume Shortlisting System built using Python and FastAPI. The application allows users to upload a resume PDF, enter the skills required for a job, and automatically evaluate the resume based on those skills.

The system identifies matching and missing skills, calculates the skill-match percentage, and determines whether the candidate is shortlisted based on a configurable threshold.

This project also demonstrates a complete DevOps workflow using Git, GitHub, Docker, Jenkins, Linux, AWS EC2, Nginx, Prometheus, and Grafana.

## Features

- Upload resume in PDF format
- Extract text from the resume
- Enter job-required skills
- Identify matching skills
- Identify missing skills
- Calculate skill-match percentage
- Configure shortlisting threshold
- Display shortlisted / not shortlisted result
- FastAPI backend
- Swagger API documentation
- Docker containerization
- Jenkins CI/CD automation
- AWS EC2 deployment
- Nginx reverse proxy
- Prometheus monitoring
- Grafana dashboards

## Technologies Used

### Application
- Python
- FastAPI
- HTML/CSS

### DevOps and Cloud
- Git
- GitHub
- Docker
- Jenkins
- Linux
- AWS EC2
- Nginx
- Prometheus
- Grafana

## Project Architecture

```text
                         Developer
                             |
                             | git push
                             v
                          GitHub
                             |
                             | Webhook
                             v
                          Jenkins
                             |
                  Build / Verify / Deploy
                             |
                             v
                           Docker
                             |
                             v
                         AWS EC2
                             |
                             v
                           Nginx
                      Reverse Proxy
                             |
                             v
                    FastAPI Application
                             |
                             v
                    Resume Shortlisting
                             |
                             v
                    Prometheus Monitoring
                             |
                             v
                       Grafana Dashboard
