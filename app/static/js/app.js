// HEMIS University System JS Utilities

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    const bgClass = type === 'success' ? 'bg-emerald-600' : (type === 'error' ? 'bg-rose-600' : 'bg-blue-600');
    toast.className = `fixed bottom-5 right-5 z-50 flex items-center gap-3 px-5 py-3 rounded-lg text-white shadow-xl ${bgClass} transition-all duration-300 transform translate-y-10 opacity-0`;
    toast.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : (type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle')} text-lg"></i>
        <span class="text-sm font-medium">${message}</span>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.remove('translate-y-10', 'opacity-0');
    }, 50);

    setTimeout(() => {
        toast.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Cascading dropdowns: load specialties and groups when faculty changes
async function updateSpecialtiesAndGroups(facultyId, specialtySelectId, groupSelectId) {
    if (!facultyId) return;
    try {
        const resp = await fetch(`/api/faculty/${facultyId}/options`);
        if (resp.ok) {
            const data = await resp.json();
            
            // Update specialties
            const spSelect = document.getElementById(specialtySelectId);
            if (spSelect) {
                spSelect.innerHTML = '<option value="">Barcha yo\'nalishlar</option>';
                data.specialties.forEach(sp => {
                    spSelect.innerHTML += `<option value="${sp.id}">${sp.code} - ${sp.name}</option>`;
                });
            }

            // Update groups
            const grpSelect = document.getElementById(groupSelectId);
            if (grpSelect) {
                grpSelect.innerHTML = '<option value="">Barcha guruhlar</option>';
                data.groups.forEach(g => {
                    grpSelect.innerHTML += `<option value="${g.id}">${g.name} (${g.course_level}-kurs)</option>`;
                });
            }
        }
    } catch (e) {
        console.error("Xatolik options yuklashda:", e);
    }
}

// Modal open/close helpers
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

