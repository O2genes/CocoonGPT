# CocoonGPT 🫁
### Professional Hyperbaric Oxygen Therapy Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

CocoonGPT is an AI-powered professional assistant specifically designed for Hyperbaric Oxygen Therapy (HBOT) operations. Built for the Cocoon HBOT chamber system, it provides role-based guidance, safety protocols, and real-time system monitoring for users, clinic staff, and operators.

![CocoonGPT Interface](docs/images/cocoongpt-interface.png)

## ✨ Features

### 🎯 **Role-Based AI Assistance**
- **Patient/User Mode**: Calming, warm guidance for HBOT newcomers
- **Clinic Staff Mode**: Professional protocols and troubleshooting
- **Operator Mode**: Technical system details and maintenance guidance

### 🏥 **Comprehensive HBOT Knowledge**
- Complete treatment protocols and safety guidelines
- FDA/UHMS approved indications and contraindications
- Cocoon-specific chamber operations and features
- Emergency procedures and risk management

### 🔧 **Real-Time System Integration**
- **Siemens S7-200 PLC** integration for chamber control
- **ESP32** connectivity for live sensor monitoring
- Real-time pressure, oxygen, temperature, and humidity tracking
- WebSocket-based live data streaming

### 🛡️ **Advanced Safety Features**
- Emergency stop protocols with immediate response
- Pressure equalization controls
- Fire safety compliance for oxygen-rich environments
- Comprehensive incident reporting and audit trails

### 💬 **Intelligent Chat Interface**
- OpenAI GPT-4 powered conversations
- Context-aware responses based on user role
- Multi-language support (extensible)
- Conversation export and audit capabilities

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Hardware      │
│   (Web App)     │    │   (Python)      │    │   Integration   │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • HTML/CSS/JS   │◄──►│ • Flask/FastAPI │◄──►│ • Siemens PLC   │
│ • Real-time UI  │    │ • OpenAI API    │    │ • ESP32 Sensors │
│ • Role Management│    │ • WebSocket     │    │ • MQTT/Modbus   │
│ • Safety Controls│    │ • Database      │    │ • Safety Systems│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+ (for frontend development)
- PostgreSQL 13+
- Redis 6+
- OpenAI API Key

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/cocoongpt.git
   cd cocoongpt
   ```

2. **Setup Python Environment**
   ```bash
   python -m venv cocoongpt_env
   source cocoongpt_env/bin/activate  # Linux/Mac
   # or
   cocoongpt_env\Scripts\activate  # Windows
   
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   nano .env
   ```

4. **Database Setup**
   ```bash
   # Create database
   createdb cocoongpt_db
   
   # Run migrations
   flask db upgrade
   ```

5. **Start the Application**
   ```bash
   # Development mode
   python app.py
   
   # Production mode
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

6. **Access the Application**
   - Open your browser to `http://localhost:3000`
   - Select your role (User/Clinic Staff/Operator)
   - Start interacting with CocoonGPT!

## 📖 Documentation

### 📋 **Knowledge Base Files**

| File | Description |
|------|-------------|
| `knowledge/hyperbaric_basics.txt` | Fundamental HBOT knowledge and principles |
| `knowledge/safety_guidelines.txt` | Comprehensive safety protocols and procedures |
| `knowledge/treatment_protocols.txt` | Standardized treatment protocols and procedures |
| `004_PLC_annotations_280525.csv` | Siemens S7-200 PLC tag annotations |

### 🎭 **User Roles**

#### 👤 **User/Patient Role**
- Receives calming, reassuring guidance
- Basic safety information and comfort measures
- Simple explanations of HBOT procedures
- Anxiety management and relaxation techniques

#### 👩‍⚕️ **Clinic Staff Role**
- Professional medical protocols and procedures
- Troubleshooting guidance for common issues
- Patient monitoring and safety checklists
- Incident reporting and documentation

#### 👨‍🔧 **Operator Role**
- Technical system operation and maintenance
- PLC programming insights and diagnostics
- Advanced troubleshooting procedures
- Equipment calibration and safety testing

### 🏥 **Treatment Modes**

| Mode | Pressure | Duration | Oxygen Delivery | Use Case |
|------|----------|----------|-----------------|----------|
| **Rest & Relax** | 1.3-1.5 ATA | 60-90 min | Continuous | Wellness, relaxation |
| **Health & Wellness** | 1.4-1.6 ATA | 90 min | Intermittent | Recovery, performance |
| **Professional Recovery** | 1.5-1.8 ATA | 90-120 min | Optimized cycles | Sports, rehabilitation |
| **Custom** | 1.0-2.0 ATA | Variable | Configurable | Medical prescriptions |
| **O2genes 100** | 1.4-1.6 ATA | 100 min | Specialized pattern | Advanced protocol |
| **O2genes 120** | 1.5-1.8 ATA | 120 min | Extended pattern | Intensive treatment |

## 🔌 Hardware Integration

### Siemens S7-200 PLC
- **Connection**: Ethernet/Serial communication
- **Protocol**: ISO-on-TCP or PPI
- **Functions**: Chamber control, safety interlocks, sensor monitoring
- **Configuration**: See `docs/plc-integration.md`

### ESP32 Sensor Interface
- **Connectivity**: WiFi/Ethernet
- **Protocols**: HTTP REST API, WebSocket, MQTT
- **Sensors**: Pressure, oxygen, temperature, humidity
- **Real-time Updates**: Sub-second sensor data streaming

### Safety Systems
- **Emergency Stop**: Hardware-level safety cutoffs
- **Fire Suppression**: Integrated with chamber controls
- **Communication**: Two-way intercom with video monitoring
- **Backup Systems**: Redundant safety mechanisms

## 🛡️ Safety & Compliance

### Medical Device Standards
- ✅ **ISO 13485** - Medical Device Quality Management
- ✅ **IEC 62304** - Medical Device Software Lifecycle
- ✅ **FDA 21 CFR Part 820** - Quality System Regulation
- ✅ **UHMS Guidelines** - Hyperbaric Medicine Standards

### Data Security
- 🔒 **GDPR Compliant** - European data protection standards
- 🔒 **HIPAA Ready** - Healthcare data privacy (US)
- 🔒 **SOC 2 Type II** - Security and availability controls
- 🔒 **ISO 27001** - Information security management

### Emergency Protocols
- 🚨 **24/7 Emergency Response** - Immediate system alerts
- 🚨 **Rapid Decompression** - Emergency pressure release
- 🚨 **Fire Safety** - Oxygen-environment fire protection
- 🚨 **Medical Emergency** - Integrated emergency procedures

## 🔧 Configuration

### Environment Variables

```bash
# Core Application
APP_NAME=CocoonGPT
APP_ENVIRONMENT=production
APP_DEBUG=false

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=500

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=cocoongpt_db
DB_USERNAME=cocoongpt_user
DB_PASSWORD=your_secure_password

# Hardware Integration
ESP32_IP_ADDRESS=192.168.1.100
PLC_IP_ADDRESS=192.168.1.50
SENSOR_UPDATE_INTERVAL=3000

# Safety Configuration
EMERGENCY_CONTACT_PRIMARY=+6588029507
CHAMBER_MAX_PRESSURE=2.0
CHAMBER_MIN_PRESSURE=1.0
```

### Cocoon Chamber Settings

```python
# Chamber physical limits
CHAMBER_LIMITS = {
    'pressure': {'min': 1.0, 'max': 2.0},  # ATA
    'temperature': {'min': 18, 'max': 26},  # Celsius
    'humidity': {'min': 30, 'max': 60},     # Percentage
    'oxygen': {'min': 21, 'max': 100}      # Percentage
}

# Default treatment parameters
DEFAULT_SETTINGS = {
    'pressure': 1.3,          # ATA
    'duration': 60,           # Minutes
    'compression_rate': 'normal',
    'oxygen_concentration': 95  # Percentage
}
```

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_safety.py -v
pytest tests/test_protocols.py -v
pytest tests/test_plc_integration.py -v
```

### Integration Tests
```bash
# Test ESP32 connectivity
pytest tests/integration/test_esp32.py

# Test PLC communication
pytest tests/integration/test_plc.py

# Test OpenAI API
pytest tests/integration/test_openai.py
```

### Safety Testing
```bash
# Emergency system tests
pytest tests/safety/test_emergency_stop.py
pytest tests/safety/test_pressure_limits.py
pytest tests/safety/test_fire_protocols.py
```

## 📊 Monitoring & Analytics

### System Metrics
- **Performance**: Response times, throughput, error rates
- **Hardware**: PLC status, sensor readings, system health
- **Usage**: Treatment sessions, user interactions, safety events
- **Business**: Patient outcomes, facility utilization, compliance

### Dashboards
- **Grafana**: Real-time system monitoring
- **Prometheus**: Metrics collection and alerting
- **Sentry**: Error tracking and performance monitoring
- **Custom**: Medical device compliance dashboards

## 🚀 Deployment

### Production Deployment

```bash
# Using Docker
docker build -t cocoongpt:latest .
docker run -p 8000:8000 --env-file .env cocoongpt:latest

# Using Docker Compose
docker-compose up -d

# Using Kubernetes
kubectl apply -f k8s/
```

### High Availability Setup

```yaml
# Load balancer configuration
services:
  - cocoongpt-app (3 replicas)
  - postgresql-primary
  - postgresql-replica
  - redis-cluster (3 nodes)
  - nginx-proxy
```

### Backup & Recovery

```bash
# Database backup
pg_dump cocoongpt_db > backup_$(date +%Y%m%d).sql

# Configuration backup
tar -czf config_backup.tar.gz .env knowledge/ static/

# Automated backup script
./scripts/backup.sh --daily
```

## 🤝 Contributing

We welcome contributions from the HBOT and medical device communities!

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   pytest
   black .
   flake8
   ```
5. **Submit a pull request**

### Contribution Guidelines

- Follow medical device development standards
- Maintain comprehensive test coverage
- Document all safety-critical changes
- Ensure HIPAA/GDPR compliance
- Update knowledge base as needed

### Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Important**: This software is for educational and research purposes. Always consult qualified medical professionals for actual patient care decisions.

## 🆘 Support

### Technical Support
- **Email**: support@o2genes.com
- **Phone**: +65 8802 9507
- **Documentation**: [docs.cocoongpt.com](https://docs.cocoongpt.com)
- **Community**: [GitHub Discussions](https://github.com/yourusername/cocoongpt/discussions)

### Emergency Support
- **24/7 Hotline**: +65 8802 9507
- **Emergency Protocol**: See `docs/emergency-procedures.md`
- **Medical Emergency**: Contact local emergency services (999 in Singapore)

### Training & Certification
- **Operator Training**: 40-hour certification program
- **Maintenance Training**: Technical systems and safety
- **Continuing Education**: Annual updates and best practices

## 🏆 Acknowledgments

### Medical Advisory Board
- Dr. [Name], Director of Hyperbaric Medicine
- Dr. [Name], Wound Care Specialist
- [Name], Certified Hyperbaric Technician

### Technology Partners
- **OpenAI** - Advanced AI language models
- **Siemens** - Industrial automation systems
- **Espressif** - ESP32 IoT platform

### Research Institutions
- Undersea & Hyperbaric Medical Society (UHMS)
- International Association for Hyperbaric Medicine
- [Your Institution/Research Partners]

## 📈 Roadmap

### Version 2.0 (Q2 2024)
- [ ] Multi-language support (Mandarin, Malay, Tamil)
- [ ] Advanced predictive analytics
- [ ] Mobile app for remote monitoring
- [ ] Integration with Electronic Health Records (EHR)

### Version 3.0 (Q4 2024)
- [ ] Voice interaction capabilities
- [ ] Augmented reality chamber guidance
- [ ] AI-powered treatment optimization
- [ ] Telemedicine integration

### Long-term Vision
- [ ] Machine learning for personalized treatments
- [ ] Global HBOT facility network
- [ ] Research data collaboration platform
- [ ] Regulatory AI for compliance automation

---

## 📞 Contact Information

**O2genes Therapy**
- **Website**: [www.o2genes.com](https://www.o2genes.com)
- **Email**: info@o2genes.com
- **Phone**: +65 8802 9507
- **Address**: [Your Business Address]

**Development Team**
- **Lead Developer**: [Your Name]
- **Medical Advisor**: [Medical Director Name]
- **Project Manager**: [PM Name]

---

*Built with ❤️ for the hyperbaric medicine community*

**Disclaimer**: This software is designed to assist healthcare professionals and should not replace qualified medical judgment. Always follow established medical protocols and consult with certified hyperbaric medicine specialists for patient care decisions.