document.addEventListener("DOMContentLoaded", () => {

  class DateTimeWidget {

    constructor() {
      this.update_date = this.update_date.bind(this);
      this.on_change = this.on_change.bind(this);

      // 🔒 Palabras clave para nunca tocar (DoB)
      this.blockedNames = ["birth", "date_of_birth", "dateofbirth", "dob"].map(s => s.toLowerCase());

      this.waitForFields();
      // referencia global para reuso en pageshow
      window.dateTimeWidgetInstance = this;
    }

    // Helpers
    isEmpty(val) {
      return val == null || String(val).trim() === "";
    }
    isBlocked(el) {
      const name = (el.getAttribute("name") || "").toLowerCase();
      const id   = (el.getAttribute("id") || "").toLowerCase();
      return this.blockedNames.some(tok => name.includes(tok) || id.includes(tok));
    }

    // 🔹 Espera dinámicamente a que los campos estén renderizados
    waitForFields() {
      let datefields = document.querySelectorAll("input[type='date']");
      let timefields = document.querySelectorAll("input[type='time']");
      if (datefields.length && timefields.length) {
        this.datefields = Array.from(datefields);
        this.timefields = Array.from(timefields);
        this.bind_fields();
        this.disable_autocomplete();
        // ❌ Eliminado el reset global de formularios
        this.autofill_now();
      } else {
        requestAnimationFrame(() => this.waitForFields());
      }
    }

    // 🔹 Enlaza eventos de cambio
    bind_fields() {
      this.datefields.forEach((el) => {
        el.addEventListener("change", this.on_change);
      });
      this.timefields.forEach((el) => {
        el.addEventListener("change", this.on_change);
      });
    }

    // 🔹 Desactiva autocompletar (Chrome ignora "off", usamos "new-password")
    disable_autocomplete() {
      this.datefields.forEach((df) => df.setAttribute("autocomplete", "new-password"));
      this.timefields.forEach((tf) => tf.setAttribute("autocomplete", "new-password"));
    }

    // 🔹 Mantengo el método pero sin tocar TinyMCE ni resetear forms globales
    reset_forms() {
      // Intencionalmente vacío: antes se hacía form.reset() y rompía TinyMCE
    }

    set_field(field, value) {
      if (!field) return;
      field.value = value;
    }

    update_date(date, time, input) {
      let ds = date ? date.value : "";
      let ts = time ? time.value : "";

      // No forzamos valores aquí (ya se establecieron en autofill si correspondía)
      if (input) {
        if (ds && ts) {
          this.set_field(input, `${ds} ${ts}`);
        } else if (ds) {
          this.set_field(input, `${ds}`);
        } else {
          this.set_field(input, "");
        }
      }
    }

    on_change(event) {
      let el = event.currentTarget;
      let target = el.getAttribute("target");
      let date = el.parentElement.querySelector("input[type='date']");
      let time = el.parentElement.querySelector("input[type='time']");
      let input = target ? document.querySelector(`input[name='${target}']`) : null;
      this.update_date(date, time, input);
    }

    // 🔹 Precarga fecha y hora actual SOLO si el campo está vacío y NO está bloqueado
    autofill_now() {
      if (!this.datefields.length || !this.timefields.length) {
        console.warn("⚠️ DateTimeWidget: no encontró inputs date/time");
        return;
      }

      let now = new Date();
      let yyyy = now.getFullYear();
      let mm = String(now.getMonth() + 1).padStart(2, "0");
      let dd = String(now.getDate()).padStart(2, "0");
      let dateStr = `${yyyy}-${mm}-${dd}`;

      let hh = String(now.getHours()).padStart(2, "0");
      let min = String(now.getMinutes()).padStart(2, "0");
      let timeStr = `${hh}:${min}`;

      // 👉 Solo establecer si el input está vacío y no está bloqueado (protege DoB y campos ya guardados)
      this.datefields.forEach((df) => {
        if (!this.isBlocked(df) && this.isEmpty(df.value)) {
          df.value = dateStr;
        }
      });
      this.timefields.forEach((tf) => {
        if (!this.isBlocked(tf) && this.isEmpty(tf.value)) {
          tf.value = timeStr;
        }
      });

      // actualiza campo oculto también, pero solo si está vacío
      this.timefields.forEach((tf) => {
        let target = tf.getAttribute("target");
        if (target) {
          let hidden = document.querySelector(`input[name='${target}']`);
          if (hidden && this.isEmpty(hidden.value)) {
            this.update_date(tf.parentElement.querySelector("input[type='date']"), tf, hidden);
          }
        }
      });
    }
  }

  // Instancia inicial
  new DateTimeWidget();

  // 🔹 Reaplicar valores si el navegador restaura formulario al volver atrás
  //     (sigue la regla: solo si están vacíos y no bloqueados)
  window.addEventListener("pageshow", () => {
    if (window.dateTimeWidgetInstance) {
      window.dateTimeWidgetInstance.autofill_now();
    }
  });

});
